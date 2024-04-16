import '../resources/app_assets.dart';

enum MenuType { line, bar, pie, scatter, radar }

extension MenuTypeTypeExtension on MenuType {
  String get displayName => '$simpleName Chart';

  String get simpleName => switch (this) {
        MenuType.line => 'Line',
        MenuType.bar => 'Bar',
        MenuType.pie => 'Pie',
        MenuType.scatter => 'Scatter',
        MenuType.radar => 'Radar',
      };

  String get documentationUrl => "Urls.getChartDocumentationUrl(this)";

  String get assetIcon => AppAssets.getChartIcon(this);
}
