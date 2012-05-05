<?php
require_once("classes/FactStore.php");

class FactStoreTest extends PHPUnit_Framework_TestCase {
    public function setUp() {
    	$this->store = new FactStore();
    }

    public function test_registers_type() {
        $this->store->register_type("WEATHER", array("Location", "Status"));
    }

    public function test_stores_one_fact() {
    	$ids = $this->store_facts(1); $id = $ids[0];
	$this->assertTrue(is_integer($id), "Should return a valid ID");
    }

    public function test_retrieves_one_fact() {
        $this->store->register_type("WEATHER", array("Location", "Status"));
	$ids = $this->store_facts(1); $id = $ids[0];
        $facts = $this->store->get_geq_id("WEATHER", $id);
	$this->assertTrue(is_array($facts), "Should return an array of facts");
	$this->assertEquals(1, count($facts), "Should return exactly one fact");
        $expected_facts = $this->get_expected_facts(1); $expected_fact = $expected_facts[0];
	$this->assertEquals($expected_fact, $facts[0], "Should return stored fact");
    }

    public function test_stores_facts_with_increasing_ids() {
        $ids = $this->store_facts(3);
        $this->assertTrue($ids[0] < $ids[1] && $ids[1] < $ids[2], "Should assign ascending ids");
    }

    public function test_stores_and_retrieves_all_facts_of_a_single_type() {
        $ids = $this->store_facts(3);
        $facts = $this->store->get_geq_id("WEATHER", $ids[0]);
	$this->assertEquals(3, count($facts), "Should return exactly three facts");
    }

    private $facts_as_arrays = array(array("Location" => "London",  "Status" => "Raining"),
                                     array("Location" => "Toronto", "Status" => "Snowing"),
                                     array("Location" => "Jakarta", "Status" => "Sunny"));

    private function store_facts($number_of_facts) {
        $ids = array();
        $this->store->register_type("WEATHER", array("Location", "Status"));
        for ($i=0; $i<$number_of_facts; $i++) {
	    $ids[] = $this->store->add("WEATHER", $this->facts_as_arrays[$i]);
        }
        return $ids;
    }

    private function get_expected_facts($number_of_facts) {
	return array_map(function($fact) { $fact["__Type"] = "WEATHER"; return $fact; }, 
                         array_slice($this->facts_as_arrays, 0, $number_of_facts));
    }
}
?>