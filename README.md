#PhotoGPSMarker
将GPX中的GPS坐标写入照片，使照片也有GPS信息了。这个工具不但支持JPEG，还支持各类相机的RAW格式。

## 使用方法
将GPX与照片放在同一个文件夹中，在命令行中执行如下命令，指定照片所在文件夹的路径。
> python gps_marker.py d:\photos

如果当前目录在照片文件夹，也可以省略照片路径。
> python c:\gps_marker.py

## 原理
GPX文件中存储在许多GPS信息，包括经度、纬度、时间、海拔等。遍历文件下的所有照片，并根据时间从GPX找到时间最接近的照片，把GPS经纬度写入照片。为了能够得与与照片拍摄地点一至的GPX，我们需要买一个GPS记录器，在拍照时一直带在身边。当我们要给照片写入GPS时，用GPS记录器相应的软件导出成GPX文件，再运行这个工具将GPX写入照片。

## 解析PGX文件
GPX其实是一个XML文件，解析它其实并不难。不过Tomo Krajina 已经写了一个解析器“gpxpy”，于是我就直接拿来用了。我们可以从[https://github.com/tkrajina/gpxpy][1]获得gpxpy。当然要使用PhotoGPSMarker，也要先安装gpxpy。

## 读写照片的EXIF
照片中的GPS信息存储在照片的EXIF头中，要想增加PGS信息必需要能读写EXIF头。我使用了开源库“pyexiv2”，作为EXIF读写工具。
可以从[http://tilloy.net/dev/pyexiv2/][2] 获得并安装。


  [1]: https://github.com/tkrajina/gpxpy
  [2]: http://tilloy.net/dev/pyexiv2/
