<?php

require 'vendor/autoload.php';

$sharedConfig = [
  'region' => 'us-east-1',
  'version' => 'latest'
];

$sdk = new Aws\Sdk($sharedConfig);

$dx = $sdk->createDataExchange();

$result = $dx->listDataSets(['Origin' => 'ENTITLED']);

foreach ($result['DataSets'] as $data_set) {
    echo $data_set['OriginDetails']['ProductId'] . '/' . $data_set['Name'] . "\n" .
      '  ' . $data_set['Description'] . "\n";
}

?>