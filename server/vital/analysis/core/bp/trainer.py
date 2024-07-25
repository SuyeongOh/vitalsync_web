import os.path
import wandb

import torch
import torch.optim as optim
from tqdm import tqdm

from server.vital.analysis.core.bp.models import *
from server.vital.analysis.core.bp.models import patcherx
from server.vital.analysis.visualizer import *


class Trainer:
    def __init__(self, config, num_train_batches):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # self.model = transformer.PPG_to_BP_Transformer().to(self.device)
        # self.model = cnn_lstm.PPG_to_BP_CNN_LSTM().to(self.device)
        # self.model = linear.PPG_to_BP_Linear().to(self.device)
        # self.model = cnn_lstm_ag.CNN_LSTM_PPG_to_BP().to(self.device)
        # self.model = transformer_ag.Transformer_PPG_to_BP().to(self.device)
        self.model = patcherx.Model().to(self.device).float()
        # weight_path = '/mnt/ssd/models/patcherx_rgb_ppg_hr_age_gender_mp_mlp/best.pth'
        # self.model.load_state_dict(torch.load(weight_path))
        self.criterion1 = torch.nn.MSELoss()
        self.criterion2 = torch.nn.L1Loss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=float(config.TRAIN.LR))
        self.scheduler = torch.optim.lr_scheduler.OneCycleLR(self.optimizer, max_lr=float(config.TRAIN.LR),
                                                             epochs=int(config.TRAIN.EPOCHS),
                                                             steps_per_epoch=num_train_batches)
        self.epochs = self.config.TRAIN.EPOCHS

        self.min_valid_loss = None
        self.best_epoch = 0

        self.visualize_flag = False

        wandb.init(
            # set the wandb project where this run will be logged
            project="ppg2bp_patcher",
            name=self.config.MODEL.NAME + '/' + '+'.join(self.config.TRAIN.LOSS) + '/' + '+'.join(
                self.config.MODEL.INPUT) + '/' + '+'.join(self.config.MODEL.TARGET),
            # track hyperparameters and run metadata
            config={
                "learning_rate": self.config.TRAIN.LR,
                "architecture": self.config.MODEL.NAME,
                "dataset": self.config.DATA.DATASET,
                "epochs": self.epochs,
                "loss": '+'.join(self.config.TRAIN.LOSS),
            }
        )

    def train(self, data_loader, num_input=1):
        mean_train_losses = []
        mean_valid_losses = []
        lrs = []
        for epoch in range(self.epochs):
            running_loss = 0.0
            train_loss = []
            self.model.train()
            tbar = tqdm(data_loader['train'])
            for idx, batch in enumerate(tbar):
                tbar.set_description("Train epoch %s" % epoch)
                self.optimizer.zero_grad()

                if num_input == 1:
                    ppg, bp = batch[0].to(self.device), batch[1].to(self.device)
                    outputs = self.model(ppg)
                elif num_input == 3:
                    ppg, age, gender, bp = (batch[0].to(self.device),
                                            batch[1].to(self.device),
                                            batch[2].to(self.device),
                                            batch[3].to(self.device))
                    outputs = self.model(ppg, age, gender)
                elif num_input == 4:
                    signal, hr, age, gender, bp = (batch[0].to(self.device),
                                                   batch[1].to(self.device),
                                                   batch[2].to(self.device),
                                                   batch[3].to(self.device),
                                                   batch[4].to(self.device))
                    outputs = self.model(signal, hr, age, gender)
                else:
                    raise ValueError("Invalid number of input")
                # if self.visualize_flag:
                # bvp_fft_plot(ppg[0].cpu().numpy(), 30)
                # print(f"Age: {age[0].cpu().numpy()}, Gender: {gender[0].cpu().numpy()}, BP: {bp[0].cpu().numpy()}")
                # self.visualize_flag = False
                # return

                # outputs = self.model(ppg)  # , age, gender)
                loss = self.criterion1(outputs, bp)  # + self.criterion2(outputs, bp)
                loss.backward()

                lrs.append(self.scheduler.get_last_lr())
                self.optimizer.step()
                self.scheduler.step()
                running_loss += loss.item()
                train_loss.append(loss.item())
                tbar.set_postfix(loss=loss.item())

            wandb.log({"epoch": epoch, "train loss": np.mean(train_loss)})
            mean_train_losses.append(np.mean(train_loss))
            valid_loss = self.valid(data_loader, False, num_input)
            wandb.log({"epoch": epoch, "valid loss": valid_loss})
            mean_valid_losses.append(valid_loss)
            if self.min_valid_loss is None:
                self.min_valid_loss = valid_loss
                self.best_epoch = epoch
                self.save_model()
                wandb.log({"epoch": epoch, "best epoch": epoch})
                best_l1_loss = self.valid(data_loader, True, num_input)
                wandb.log({"best l1 loss": best_l1_loss})
                # wandb.log({"epoch": epoch,"best sbp loss": sbp_loss})
                # wandb.log({"epoch": epoch,"best dbp loss": dbp_loss})
                print(f"Update Best Model at epoch {epoch}")
            elif valid_loss < self.min_valid_loss:
                self.min_valid_loss = valid_loss
                self.best_epoch = epoch
                self.save_model()
                wandb.log({"epoch": epoch, "best epoch": epoch})
                best_l1_loss = self.valid(data_loader, True, num_input)
                wandb.log({"epoch": epoch, "best l1 loss": best_l1_loss})
                # wandb.log({"epoch": epoch, "best sbp loss": sbp_loss})
                # wandb.log({"epoch": epoch, "best dbp loss": dbp_loss})
                print(f"Update Best Model at epoch {epoch}")

    def valid(self, data_loader, l1_flag=False, num_input=1):
        valid_loss = []
        valid_sbp_loss = []
        valid_dbp_loss = []
        self.model.eval()
        with torch.no_grad():
            vbar = tqdm(data_loader["valid"])
            for valid_idx, valid_batch in enumerate(vbar):
                vbar.set_description("Validating")
                if num_input == 1:
                    ppg, bp = valid_batch[0].to(self.device), valid_batch[1].to(self.device)
                    outputs = self.model(ppg)
                elif num_input == 3:
                    ppg, age, gender, bp = valid_batch[0].to(self.device), valid_batch[1].to(self.device), valid_batch[
                        2].to(self.device), valid_batch[3].to(self.device)
                    outputs = self.model(ppg, age, gender)
                elif num_input == 4:
                    signal, hr, age, gender, bp = valid_batch[0].to(self.device), valid_batch[1].to(self.device), valid_batch[2].to(self.device), valid_batch[3].to(self.device), valid_batch[4].to(self.device)
                    outputs = self.model(signal, hr, age, gender)
                else:
                    raise ValueError("Invalid number of input")
                if l1_flag:
                    loss = self.criterion2(outputs, bp)
                    # sbp_loss = self.criterion2(outputs[:, 0], bp[:, 0])
                    # dbp_loss = self.criterion2(outputs[:, 1], bp[:, 1])
                    # valid_sbp_loss.append(sbp_loss.item())
                    # valid_dbp_loss.append(dbp_loss.item())
                else:
                    loss = self.criterion1(outputs, bp)  # + self.criterion2(outputs, bp)
                valid_loss.append(loss.item())
                vbar.set_postfix(loss=loss.item())
            valid_loss = np.mean(valid_loss)
            if l1_flag:
                # valid_sbp_loss = np.mean(valid_sbp_loss)
                # valid_dbp_loss = np.mean(valid_dbp_loss)
                # print(f"Validating L1 Loss: {valid_loss}, SBP Loss: {valid_sbp_loss}, DBP Loss: {valid_dbp_loss}")
                return valid_loss  # , valid_sbp_loss, valid_dbp_loss
        return valid_loss

    def save_model(self):
        save_path = self.config.MODEL.SAVE_PATH + self.config.MODEL.NAME + '_'.join(self.config.MODEL.INPUT) + '_'.join(
            self.config.MODEL.TARGET)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        model_path = os.path.join(save_path, f"best.pth")
        torch.save(self.model.state_dict(), model_path)
