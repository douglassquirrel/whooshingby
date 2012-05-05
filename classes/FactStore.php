<?php
class FactStore {
    function __construct() {
        $this->repo = array();
    }

    function register_type($type) {}

    function add($type, $fact_array) {
        $fact_array["__Type"] = $type;
        $this->repo[] = $fact_array;
	return count($this->repo);
    }

    function get_geq_id($id) {
        return $this->repo;
    }
}
?>