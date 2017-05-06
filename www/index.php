<?php
$max = 100; $min = 10;
$num1 = random_int ($min,$max );
$num2 = random_int ($min,$max );
$key = "SeJxTPXigSWhbJK23MrY";
$key2 = "DWUTQI0MceaSBVutsoR1";
$ipAddress = $_SERVER['REMOTE_ADDR'];
$nonce = time();
$total = $num1 + $num2;
$image = @imagecreatetruecolor(120, 45);
$background = imagecolorallocate($image, 0x00, 0x00, 0x84);
imagefill($image, 0, 0, $background);
$linecolor = imagecolorallocate($image, 0x00, 0x00, 0x00);
$textcolor = imagecolorallocate($image, 0xFF, 0xFF, 0xFF);
  $font = '/var/www/bot.ttf';
  $digit = '';
  for($i=0; $i < 120; $i++) {
    imagesetthickness($image, rand(1,5));
    $linecolor = imagecolorallocate($image, random_int(0,128), random_int(0,128),random_int(0,128));
    imageline($image, 0, random_int(0,70), 120, random_int(0,70), $linecolor);
  }

  for($x = 15; $x <= 95; $x += 20) {
    $digit .= ($num = random_int(0, 9));
    //imagechar($image, $font, $x, random_int(2, 14), $num, $textcolor);
    imagettftext($image, 26, random_int(0,20), $x, 35, $textcolor, $font, $num);
  }

  $authcode = hash("sha256", $key . $nonce . $ipAddress . $digit . $key2);
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>HATNAS v1.337</title>
    <meta name="description" content="A Public Hat Based NAS">
    <meta name="author" content="Forrest Fuqua AKA JetBalsa">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="/css/bootstrap.min.css" rel="stylesheet">
    <link href="/res/bootstrap.min.css" rel="stylesheet">
    <link href="/res/crashoverride.css" rel="stylesheet">
  </head>
  <body><div class="container">
  <div class="row"><br><br><br><!-- DEM BRs I'm a PHP Programmer, not a UI Designer :P -->
        <div class="col-md-6 center-block trans-bg">
	<a href="/"><img src="/res/hatnas.png"></a><br><br><br><br>
        <div class="col-md-6">
        <div class="btn-group">
  	<a href="/" class="btn btn-default">Upload a File</a>
  	<a href="/about.php" class="btn btn-default trans-bg">About</a>
  	<a href="/list.php" class="btn btn-default trans-bg">File List</a></div>
        <br><br>
<form role="form" class="form-horizontal" action="/upload.php" method="POST" enctype="multipart/form-data">
  <div class="form-group">
     <label for="InputName">Hacker Name:</label>
    <input type="text" class="form-control" id="InputName" name="InputName" required placeholder="Hacker Name">
    <p class="help-block">A-Z,a-z,0-9, 16</p>
  </div>
  <div class="form-group">
    <label for="InputName">Folder:</label>
     <select class="form-control" name="folder">
      <option value="1">Other</option>
      <option value="2">Images</option>
      <option value="3">Porn</option>
      <option value="4">Books / Text</option>
      <option value="5">Tools</option>
      <option value="6">Code</option>
      <option value="7">Videos</option>
      <option value="8">Music</option>
      </select>
  </div>
  <div class="form-group"><!-- NEEDS MAOR JPEG -->
    <label for="AntiHatHax">Enter Code:<br><?php echo gdImgToHTML($image); ?></label>
    <input type="number" class="form-control" id="AntiHatHax" required name="AntiHatHax">
  </div>
  <div class="form-group">
    <label for="userFile">File<br><ul><li>You may want to access this in a proper browser<br>Any HTTP website will be redirected back to here</li><li>Don't be a complete dick<br>Mark dangerous uploads please.</li></ul></label>
    <input type="file" id="userFile" name="userFile" required placeholder="C:\NSASECRETS.TXT">
</label>
    <p class="help-block">A-Z,a-z,0-9, 16.4, 25MB</p>
  </div>
  <input type="hidden" name="AntiHatHaxHash" value="<?php echo $nonce . ":" . $authcode; ?>">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <button type="submit" class="btn btn-success">Submit</button>
</form><br>
</div>


        </div>
  </div></div>



   <script src="/js/jquery.min.js"></script>
   <script src="/js/bootstrap.min.js"></script>
  </body>
</html>

<?php
function gdImgToHTML( $gdImg, $format='jpg' ) {

    // Validate Format
    if( in_array( $format, ['jpg', 'jpeg', 'png', 'gif'] ) ) {

        ob_start();

        if( $format == 'jpg' || $format == 'jpeg' ) {

            imagejpeg( $gdImg, NULL, 1);

        } elseif( $format == 'png' ) {

            imagepng( $gdImg );

        } elseif( $format == 'gif' ) {

            imagegif( $gdImg );
        }

        $data = ob_get_contents();
        ob_end_clean();

        // Check for gd errors / buffer errors
        if( !empty($data) ) {

            $data = base64_encode( $data );

            // Check for base64 errors
            if ( $data !== false ) {

                // Success
                return "<img alt='Refresh Page to get new code' src='data:image/$format;base64,$data'>";
            }
        }
    }

    // Failure
    return '<div class="alert alert-danger">Anti-Bot Failed to load! Find the owner!</div>';
}

