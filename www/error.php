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
switch ($_GET['code']) {
case 413:
echo "<div class='alert alert-danger' role='alert'>File Upload Error, File too large!<div>";
break;

case 404:
echo "<div class='alert alert-danger' role='alert'>File not Found, You might want to look for it in the digital grave yard<div>";
break;

case 500:
echo "<div class='alert alert-danger' role='alert'>You broke HATNAS?! Good Job! Report this to the owner!<div>";
break;

default:
echo "<div class='alert alert-danger' role='alert'>Unknown error! Please try your request again!<div>";

}
?>
  </div></div>



   <script src="/js/jquery.min.js"></script>
   <script src="/js/bootstrap.min.js"></script>
  </body>
</html>
