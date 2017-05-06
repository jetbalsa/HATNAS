<?php
	$sock = @fsockopen("127.0.0.1", "2947", $errno, $errstr, 2);
		@fwrite($sock, "?WATCH={\"enable\":true}\n");
		usleep(1000);
		@fwrite($sock, "?POLL;\n");
		usleep(1000);
		for($tries = 0; $tries < 10; $tries++){
			$resp = @fread($sock, 2000); # SKY can be pretty big
			if (preg_match('/{"class":"POLL".+}/i', $resp, $m)){
				$resp = $m[0];
				break;
			}
		}
		@fclose($sock);
		if (!$resp){
			$resp = '{"class":"ERROR","message":"no response from GPS daemon"}';}

file_put_contents("/tmp/gps.json", $resp);
