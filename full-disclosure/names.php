<?php

$xml = simplexml_load_file( 'small_product_data.xml' );

$mapping = array();

foreach ( $xml->product as $product ) {
	//echo $product->name;
	//echo " ---> ";
	//echo $product->sku . "\n" ;
	
	$sku = (int) $product->sku;
	$name = (string) $product->name;
	
	$mapping[$sku] = $name;
}

asort( $mapping );	// in place

foreach ( $mapping as $sku => $name ) {
	$data .= "$sku\t$name\n";
}
	
file_put_contents( 'sku_name.tsv', $data );