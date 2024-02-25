import ogc_python_tools.ogc_python_logging as l

DEFAULT_LOGGING_STATE = l.INFO

if __name__ == "__main__":
    # setup logging
    l.threshold_set( DEFAULT_LOGGING_STATE ) # set logging threashold to some default state
    l.storage_use_set( True ) # set storage buffer for use in TUI
    l.log_file_set( "ogc-network-mqtt-tui.log" ) # create a file to save logs

    l.log( l.INFO, "OGC.Engineering - ogc-network-mqtt-tui started" )
    # do something
    l.log( l.INFO, "OGC.Engineering - ogc-network-mqtt-tui ended" )
