<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>HATNAS v1.337 | About</title>
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
        <br><br></div></div></div>



<?php
$hathaxascii = <<<'EOF'
<center><img class="blink" src="/res/hathax.png"></center>
</div>
EOF;

if($_SERVER['REQUEST_METHOD'] != "POST"){die("<div class='alert alert-danger' role='alert'>$hathaxascii");}
if(empty($_POST["InputName"])){die("<div class='alert alert-danger' role='alert'>Please put in a Hacker Name");}
if(empty($_POST["AntiHatHaxHash"])){die("<div class='alert alert-danger' role='alert'>$hathaxascii");}
if(empty($_POST["AntiHatHax"])){die("<div class='alert alert-danger' role='alert'>Please solve the Anti-Bot Code");}
if(empty($_POST["folder"])){die("<div class='alert alert-danger' role='alert'>$hathaxascii");}

$fnum = preg_replace("/[^0-9]:+/i", "", $_POST["folder"]);
if(strlen($fnum) > 1){die("<div class='alert alert-danger' role='alert'>$hathaxascii");}
if(strlen($_POST["AntiHatHaxHash"]) > 256){die("<div class='alert alert-danger' role='alert'>$hathaxascii");}
if(strlen($_POST["AntiHatHax"]) > 5){die("<div class='alert alert-danger' role='alert'>Invaild AntiHatHax Code");}

$haxhash = preg_replace("/[^a-z0-9]:+/i", "", $_POST["AntiHatHaxHash"]);
$total = preg_replace("/[^0-9]+/i", "", $_POST["AntiHatHax"]);

$key = "SeJxTPXigSWhbJK23MrY";
$key2 = "DWUTQI0MceaSBVutsoR1";
$ipAddress = $_SERVER['REMOTE_ADDR'];

$x = (explode(":",$_POST["AntiHatHaxHash"]))[0];
$hash = (explode(":",$_POST["AntiHatHaxHash"]))[1];

if(empty($x)){die("<div class='alert alert-danger' role='alert'>$hathaxascii");}
if(empty($hash)){die("<div class='alert alert-danger' role='alert'>$hathaxascii");}

$expire = time() - 600;

if($x < $expire){die("<div class='alert alert-danger' role='alert'>$hathaxascii");}

$authcode = hash("sha256", $key . $x . $ipAddress . $total . $key2);

if(hash_equals($authcode, $hash) === FALSE){die("<div class='alert alert-danger' role='alert'>Invaild AntiHatHax Code, Go back and try again");}

switch ($fnum) {
case 1:
$folder = "other";
break;

case 2:
$folder = "images";
break;

case 3:
$folder = "porn";
break;

case 4:
$folder = "text";
break;

case 5:
$folder = "tools";
break;

case 6:
$folder = "code";
break;

case 7:
$folder = "videos";
break;

case 8:
$folder = "music";
break;


default:
die("<div class='alert alert-danger' role='alert'>$hathaxascii");

}


if(file_exists('/mnt/usb/l/hash/' . $authcode)){
	die("<div class='alert alert-danger' role='alert'>Invaild AntiHatHax Code[CTRL+F5 the page! Your Key was old!]");
}else{
	file_put_contents('/mnt/usb/l/hash/' . $authcode, time());
}
 
$info = pathinfo($_FILES["userFile"]["name"]);
$file_name =  $info['filename'];
$hackername = substr(preg_replace("/[^a-z0-9]+/i", "", $_POST["InputName"]), 0, 16); 
$filename = substr(preg_replace("/[^a-z0-9]+/i", "", $file_name),0, 16);
$ext = substr(preg_replace("/[^a-z0-9]+/i", "", $info['extension']),0, 4);
if(strlen($hackername) < 2){die("<div class='alert alert-danger' role='alert'>Hacker Name must be more then 2 letters after filtering");}
if(strlen($filename) < 4){die("<div class='alert alert-danger' role='alert'>Filename must be more then 4 letters after filtering");}
if(strlen($ext) < 1){die("<div class='alert alert-danger' role='alert'>Filename Ext must be more then 1 letter after filtering");}

$uploaddir = '/mnt/usb/u/' . $folder. "/";

$target_file = $uploaddir . $hackername . "-" . $filename . "." . $ext;
if (file_exists($target_file)) {
    echo "<div class='alert alert-danger' role='alert'>Sorry, file already exists.";
    die();
}
$fp = fopen("/mnt/usb/listindex.txt", "r+");
$numfile = '/mnt/usb/l/num/' . $folder. "/" . $hackername . "-" . $filename . "." . $ext;
if (flock($fp, LOCK_EX)) {
$indexnumber = file_get_contents("/mnt/usb/index.txt");
$indexnumber++;
$list = file_get_contents("/mnt/usb/listindex.txt");
$list .= "$indexnumber|$target_file".PHP_EOL;
file_put_contents("/mnt/usb/listindex.txt", $list);
file_put_contents("/mnt/usb/index.txt", $indexnumber);
flock($fp, LOCK_UN);
} else {
    die("<div class='alert alert-danger' role='alert'>Sorry, Couldn't get DB Lock, Try Upload Again");
}
fclose($fp);

    if (move_uploaded_file($_FILES["userFile"]["tmp_name"], $target_file)) {
        echo "<div class='alert alert-success' role='alert' style='color: black;'>The file ". $hackername . "-" . $filename . "." . $ext . " has been uploaded.<br><a href='/list.php'>Check out the File List</a>";
    } else {
        echo "<div class='alert alert-danger' role='alert'>Sorry, there was an error uploading your file. Go tell the owner (Look for the Pith Helmet!)";
    }

?>
        <br></div>


        </div>
  </div></div>



   <script src="/js/jquery.min.js"></script>
   <script src="/js/bootstrap.min.js"></script>
  </body>
</html>
