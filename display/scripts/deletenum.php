<?php
$list = file("/mnt/usb/listindex.txt");
foreach($list as $row){
$file[(explode("|", $row))[0]] = trim((explode("|", $row))[1]);
}
if(empty($argv[2])){
unlink($file[$argv[1]]);
}else{
rename($file[$argv[1]], "/mnt/usb/l/num/" . basename($file[$argv[1]]) . "." . time());
}

echo "File " . basename($file[$argv[1]]) . " Removed".PHP_EOL;


