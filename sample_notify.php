<?php

if ($_POST['notifyText'] && ($_POST['key'] == 'jsdlljdshf3e3wr___randomkey___jsdhjsdhfkdjsf3q4')) {
	$message = $_POST['notifyText'];
	$url = "https://hooks.slack.com/services/___webhook___URL";
	$postdata = 	array(	'text' => $message,
			'username' => 'computerlocation',
			'icon_emoji' => ':lightning:'
			);

	$json = json_encode($postdata);

	$curl = curl_init($url);
	curl_setopt($curl, CURLOPT_HEADER, false);
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($curl, CURLOPT_HTTPHEADER,
        	array("Content-type: application/json"));
	curl_setopt($curl, CURLOPT_POST, true);
	curl_setopt($curl, CURLOPT_POSTFIELDS, $json);

	$json = json_encode($postdata);

	$json_response = curl_exec($curl);

	curl_close($curl);
} else {
	die();
}

?>