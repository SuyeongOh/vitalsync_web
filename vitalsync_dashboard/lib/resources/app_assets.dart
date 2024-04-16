import 'package:vitalsync_dashboard/utils/app_helper.dart';

class AppAssets {
  static String getChartIcon(MenuType type) {
    switch (type) {
      case MenuType.line:
        return 'assets/icons/ic_line_chart.svg';
      case MenuType.bar:
        return 'assets/icons/ic_bar_chart.svg';
      case MenuType.pie:
        return 'assets/icons/ic_pie_chart.svg';
      case MenuType.scatter:
        return 'assets/icons/ic_scatter_chart.svg';
      case MenuType.radar:
        return 'assets/icons/ic_radar_chart.svg';
    }
  }

  static const flChartLogoIcon = 'assets/icons/fl_chart_logo_icon.png';
  static const flChartLogoText = 'assets/icons/fl_chart_logo_text.svg';
}
