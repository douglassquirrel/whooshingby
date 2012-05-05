<?php
require_once("classes/FactStore.php");

class FactStoreTest extends PHPUnit_Framework_TestCase {
    public function test_registers_type() {
        $store = new FactStore();
        $store->register_type("WEATHER", array("Location", "Status"));
    }

    public function test_stores_one_fact() {
        $store = new FactStore();
        $store->register_type("WEATHER", array("Location", "Status"));
	$id = $store->add("WEATHER", array("Location" => "London", "Status" => "Raining"));
	$this->assertTrue(is_integer($id), "Should return a valid ID");
    }

    public function test_retrieves_one_fact() {
        $store = new FactStore();
        $store->register_type("WEATHER", array("Location", "Status"));
	$id = $store->add("WEATHER", array("Location" => "London", "Status" => "Raining"));
        $facts = $store->get_geq_id("WEATHER", $id);
	$this->assertTrue(is_array($facts), "Should return an array of facts");
	$this->assertEquals(1, count($facts), "Should return exactly one fact");
	$fact = $facts[0];
	$this->assertEquals(array("__Type" => "WEATHER", "Location" => "London", "Status" => "Raining"), $fact, "Should return stored fact");
    }
}
?>