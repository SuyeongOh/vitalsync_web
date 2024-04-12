import 'package:dartx/dartx.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../cubits/app/app_cubit.dart';
import '../resources/app_colors.dart';
import 'menu_row.dart';

class SideBar extends StatefulWidget{

  @override
  State createState() => AppMenuState();
}

class AppMenuState extends State<SideBar> {
  @override
  Widget build(BuildContext context) {
    return Container(
      color: AppColors.itemsBackground,
      child: Column(
        children: [
          SafeArea(
            child: AspectRatio(
              aspectRatio: 3,
              child: Center(
                child: InkWell(
                  onTap: widget.onBannerClicked,
                  child: const FlChartBanner(),
                ),
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemBuilder: (context, position) {
                final menuItem = widget.menuItems[position];
                return MenuRow(
                  text: menuItem.text,
                  svgPath: menuItem.iconPath,
                  isSelected: widget.currentSelectedIndex == position,
                  onTap: () {
                    widget.onItemSelected(position, menuItem);
                  },
                  onDocumentsTap: () async {
                    final url = Uri.parse(menuItem.chartType.documentationUrl);
                  },
                );
              },
              itemCount: widget.menuItems.length,
            ),
          ),
          const _AppVersionRow(),
        ],
      ),
    );
  }
}

class _AppVersionRow extends StatelessWidget {
  const _AppVersionRow();

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<AppCubit, AppState>(builder: (context, state) {
      if (state.appVersion.isNullOrBlank) {
        return Container();
      }
      return Container(
        margin: const EdgeInsets.all(12),
        child: Row(
          children: [
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(10.0),
                child: RichText(
                  text: TextSpan(
                    text: '',
                    style: DefaultTextStyle.of(context).style,
                    children: <TextSpan>[
                      const TextSpan(text: 'App version: '),
                      TextSpan(
                        text: 'v${state.appVersion!}',
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      if (state.usingFlChartVersion.isNotBlank) ...[
                        TextSpan(
                          text: '\nfl_chart: ',
                          recognizer: TapGestureRecognizer()
                            ..onTap = BlocProvider.of<AppCubit>(context)
                                .onVersionClicked,
                        ),
                        TextSpan(
                          text: 'v${state.usingFlChartVersion}',
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                          ),
                          recognizer: TapGestureRecognizer()
                            ..onTap = BlocProvider.of<AppCubit>(context)
                                .onVersionClicked,
                        ),
                      ]
                    ],
                  ),
                ),
              ),
            ),
            state.availableVersionToUpdate.isNotBlank
                ? TextButton(
              onPressed: () {},
              child: Text(
                'Update to ${state.availableVersionToUpdate}',
                style: const TextStyle(
                  color: AppColors.primary,
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                ),
              ),
            )
                : TextButton(
              onPressed: () => (),
              child: const Text(
                'About',
                style: TextStyle(
                  color: AppColors.primary,
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
      );
    });
  }
}