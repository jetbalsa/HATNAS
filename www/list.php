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
  	<a href="/" class="btn btn-default trans-bg">Upload a File</a>
  	<a href="/about.php" class="btn btn-default trans-bg">About</a>
  	<a href="/list.php" class="btn btn-default">File List</a></div>
        <br><br>
        <br></div></div></div><div class="trans-bg"><div class="col-md-6"><div class="trans-bg-2">
<div class="alert alert-danger slowblink"><center>
  <strong>Danger!</strong> Do not trust any of the files listed below!
</center></div>

<ul>
<?php

$fa = dirToArray("/mnt/usb/u/");
array_shift($fa);
foreach($fa as $key => $folder){
echo "<li>$key" . PHP_EOL;
foreach($folder as $file){
echo "<ul>";
echo "<li><a href='/u/$key/$file'>$file</a>  " . human_filesize(filesize("/mnt/usb/u/$key/$file"), 1) . "</li>" . PHP_EOL;
echo "</ul>";
}
echo "</li>";
}
function human_filesize($bytes, $decimals = 2) {
  $sz = 'BKMGTP';
  $factor = floor((strlen($bytes) - 1) / 3);
  return sprintf("%.{$decimals}f", $bytes / pow(1024, $factor)) . @$sz[$factor];
}

function dirToArray($dir) {
  
   $result = array();

   $cdir = scandir($dir);
   foreach ($cdir as $key => $value)
   {
      if (!in_array($value,array(".","..")))
      {
         if (is_dir($dir . DIRECTORY_SEPARATOR . $value))
         {
            $result[$value] = dirToArray($dir . DIRECTORY_SEPARATOR . $value);
         }
	else{
	    $result[] = $value;
	}
      }
   }
  
   return $result;
} 
?>
</ul><br><br><br>
<div></div>

        </div>
  </div></div>



   <script src="/js/jquery.min.js"></script>
   <script src="/js/bootstrap.min.js"></script>
  </body>
</html>
