<?php
require_once("classes/FactStore.php");

class FactStoreTest extends PHPUnit_Framework_TestCase {
    public function test_stores_one_fact() {
        $store = new FactStore();
	$store->add("WEATHER", "Raining");
    }
}
?>