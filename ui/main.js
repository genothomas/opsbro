/**************************************
 Server Elections
 *************************************/
    
    
    // If there is no servers in the config, take the http addr
var server   = null;
var def_port = 6768;


if ( servers.length == 0 ) {
    var p = parse_uri( window.location );
    servers.push( p.hostname + ':' + def_port );
}


// Do not connect always to the same first server, let a chance for other to manage the load
servers.shuffle();

console.debug( 'GET SERVERS' + servers );

// Our list of servers and their states
var pot_servers = {};


$.each( servers, function( _idx, s ) {
    var elts     = s.split( ":" );
    var hostname = s;
    var port     = def_port;
    console.log( elts );
    if ( elts.length > 1 ) {
        hostname = elts[ 0 ];
        port     = parseInt( elts[ 1 ] );
    }
    else {
        s = s + ':' + def_port;
    }
    var ws_port      = port + 1;
    pot_servers[ s ] = {
        'state'  : 'pending',
        'uri'    : s,
        port     : port,
        ws_port  : ws_port,
        hostname : hostname,
        'elected': false
    };
} );


function update_connections_view() {
    var ul              = $( '#connections-ul' );
    var connections_tpl = get_template( 'tpl-connections-list' );
    // get connections but as list for mustache
    var connections     = dict_get_values( pot_servers );
    var s_connections   = Mustache.render( connections_tpl, { connections: connections } );
    ul.html( s_connections );
}


$( function() {
    update_connections_view();
} );


// We will look at all servers and take the first that answer us
function elect_server() {
    $.each( pot_servers, function( s ) {
        var uri                       = "http://" + s;
        pot_servers[ s ][ 'state' ]   = 'pending';
        pot_servers[ s ][ 'elected' ] = false; // clean all previous elected thing
        $.ajax( {
            url: uri
        } )
         .error( function() {
             console.log( 'PING fail to the server: ' + s );
             pot_servers[ s ][ 'state' ] = 'error';
             update_connections_view();
         } )
         .done( function() {
             console.log( 'Connexion OK to the server: ' + s );
             pot_servers[ s ][ 'state' ] = 'ok';
             if ( server == null ) {
                 console.log( 'We just elected a new server: ' + s );
                 server = s;
             }
             // If we choose or kept this server as elected, say it
             if ( server == s ) {
                 pot_servers[ s ][ 'elected' ] = true; // clean all previous elected thing
             }
             update_connections_view();
         } );
    } );
}


elect_server();


// Main structure to put nodes
var nodes    = [];
var selected = '';


/***********************************************************
 *                         Node                            *
 ***********************************************************/

var __Node_properties = [ 'uuid', 'addr', 'checks', 'incarnation', 'name', 'port', 'state', 'tags' ];  // to copy from gossip
function Node( gossip_entry ) {
    // Get properties directly from gossip objects
    this.update( gossip_entry );
    
    // and display properties
    this.V_li_bloc = null;  // view li bloc
}


Node.prototype.update = function( gossip_entry ) {
    for ( var i = 0; i < __Node_properties.length; i++ ) {
        var k     = __Node_properties[ i ];
        this[ k ] = gossip_entry[ k ];
    }
};


Node.prototype.tostr = function() {
    console.log( this );
    var s = 'Node:: ';
    for ( var i = 0; i < __Node_properties.length; i++ ) {
        var k = __Node_properties[ i ];
        s += ' [' + k + '=' + this[ k ] + ']';
    }
    return s;
};


Node.prototype.update_and_show_detail = function() {
    // We got a click, tag the selected element
    selected = this.uuid;
    
    // first header, we have enough data for this
    var detail_header_tpl = get_template( 'tpl-detail-header' );
    var s_detail_header   = Mustache.to_html( detail_header_tpl, this );
    $( '#detail-header' ).html( s_detail_header );
    
    
    var now = new Date().getTime();
    
    var srv = this.addr + ':' + this.port;
    // Node detail + checks
    $.getJSON( "http://" + srv + "/agent/state/" + this.uuid + '?_t=' + now, function( data ) {
        // now checks
        var detail_checks_tpl = get_template( 'tpl-detail-checks' );
        var s_detail_checks   = Mustache.to_html( detail_checks_tpl, { 'checks': dict_get_values( data.checks ) } );
        $( '#detail-checks' ).html( s_detail_checks );
        
    } );
    
    // Agent informations + information
    $.getJSON( 'http://' + srv + '/agent/info?_t=' + now, function( data ) {
        // first agent information
        var detail_information_tpl = get_template( 'tpl-detail-information' );
        var s_detail_information   = Mustache.to_html( detail_information_tpl, data );
        $( '#detail-information' ).html( s_detail_information );
        
        // and collectors basic information (more information with metrics will need more additional calls)
        var detail_collectors_tpl = get_template( 'tpl-detail-collectors-list' );
        var s_detail_collectors   = Mustache.to_html( detail_collectors_tpl, { 'collectors': dict_get_values( data.collectors ) } );
        $( '#detail-collectors-list' ).html( s_detail_collectors );
    } );
    
    // Detectors informations
    $.getJSON( 'http://' + srv + '/agent/detectors/?_t=' + now, function( data ) {
        // first agent information
        var detail_detectors_tpl = get_template( 'tpl-detail-detectors' );
        var s_detail_detectors   = Mustache.to_html( detail_detectors_tpl, { 'detectors': data } );
        $( '#detail-detectors' ).html( s_detail_detectors );
    } );
    
    // Collectors informations
    $.getJSON( 'http://' + srv + '/collectors/?_t=' + now, function( data ) {
        var data_str = '';
        for ( var k in data ) {
            if ( data.hasOwnProperty( k ) ) {
                var collector_data_id = "collector-data-" + k;
                var k_s               = '<div class="collector-data-cont" >';
                k_s += '<a href="javascript:show_collector(\'' + k + '\')">' + k + '</a>';
                var results           = data[ k ].results;
                
                function tree_to_string( r ) {
                    var s = '';
                    if ( typeof r == 'object' ) {
                        s = '<ul>';
                        for ( var k2 in r ) {
                            if ( r.hasOwnProperty( k2 ) ) {
                                s += '<li>' + k2;
                                s += tree_to_string( r[ k2 ] );
                                s += '</li>';
                            }
                        }
                        s += '</ul>';
                    }
                    else {
                        if ( r == '' ) {
                            r = '""';
                        }
                        s = ' => ' + r;
                    }
                    return s;
                }
                
                k_s += '<div class="collector-data" id="' + collector_data_id + '" >';
                k_s += tree_to_string( results );
                k_s += '</div>';
                k_s += '</div>';
            }
            data_str += k_s;
        }
        $( '#detail-collectors-data' ).html( data_str );
    } );
    
};


// Generate a LI string with the host information
Node.prototype.generate_host_list_entry = function() {
    var node_bloc_tpl = get_template( 'tpl-node-bloc' );
    var s             = Mustache.to_html( node_bloc_tpl, this );
    var li            = $( s );
    // link the node on the li object
    li.data( 'node', this );
    
    // and link click on the li
    li.on( 'click', function() {
        var this_node = $( this ).data( 'node' ); // this == the li object here
        // First clean detail parts
        clean_detail();
        this_node.update_and_show_detail();
        open_right_panel();
    } );
    
    // Save the dom li bloc on the node data
    this.V_li_bloc = li;
    
    return li;
};

// Hide/show functions for the li
Node.prototype.hide = function() {
    this.V_li_bloc.hide();
};
Node.prototype.show = function() {
    this.V_li_bloc.show();
};


function load_nodes() {
    add_spinner( '#nodes' );
    var now = new Date().getTime();
    $.getJSON( "http://" + server + "/agent/members?_t=" + now, function( data ) {
        // First put all nodes into our list
        $.each( data, function( key, val ) {
            var n = new Node( val );
            console.debug( n.tostr() );
            nodes.push( n );
        } );
        refresh_nodes();
    } );
}


// Hide others main part, update menu and show the one desired
function show_main_part( part ) {
    // Hide
    $( '#list-left > .main-part' ).hide();
    
    // clean menu
    $( '#menu .menu-a' ).removeClass( 'active' );
    
    // Show main part
    $( '#' + part ).show();
    
    // and menu one
    $( '#' + part + '-btn' ).addClass( 'active' );
    
}


// Count the number of node and service, and update the btn badges
function update_counts() {
    $( '#badge-nodes' ).html( nodes.length );
}


function sort_lists() {
    sort_lists_for();
}


function sort_lists_for() {
    var mylist    = $( '#nodes > ul' );
    var listitems = mylist.children( 'li' ).get();
    listitems.sort( function( a, b ) {
        return $( a ).attr( 'id' ).localeCompare( $( b ).attr( 'id' ) );
    } );
    $.each( listitems, function( idx, itm ) {
        mylist.append( itm );
    } );
}


function apply_filters() {
    var reg          = $( "#filter-value" ).val();
    var filter_state = $( "#filter-state" ).val();
    
    var look_for = 'name';
    // For nodes we can look for others things
    // Look at filter type
    if ( reg.startsWith( 't:' ) ) {
        console.debug( 'MATCH TAG' );
        look_for = 'tags';
        var tag  = reg.replace( 't:', '' );
        // if void tag, exit
        if ( tag == '' ) {
            return;
        }
    }
    
    // look for all nodes, and apply filter.
    // to be shown, must match name filter AND state filter
    // so any bad filter means hide
    for ( var i = 0; i < nodes.length; i++ ) {
        var node    = nodes[ i ];
        var name    = node.name;
        var e_state = node.state;
        
        // We must match both name/tag and state
        // First name, bail out if no match
        if ( look_for == 'name' ) {
            if ( !(name.indexOf( reg ) > -1) ) {
                node.hide();
            }
            else {
                node.show();
            }
        }
        else {
            var founded = false;
            for ( var j = 0; j < node.tags.length; j++ ) {
                if ( reg == node.tags[ j ] ) {
                    founded = true;
                }
            }
            if ( founded ) {
                node.show();
            }
            else {
                node.hide();
            }
        }
        
        /* CASSE
         // Here, the name match was not need or false,
         // so look at the state
         if ( (state == 'any value') ||
         ((state == 'passing') && (e_state == 'alive')) ||
         ((state == 'failing') && (e_state == 'leave' || e_state == 'dead' || e_state == 'suspect'))
         ) {
         node.show();
         } else {
         node.hide();
         }
         */
        
    }
    
    
}

// Binding the filtering part
$( function() {
    
    // By default show the nodes
    $( '#nodes' ).hide();
    
    apply_filters();
    
    $( "#filter-value" ).bind( 'input', function() {
        apply_filters();
    } );
    
    $( "#filter-state" ).on( 'change', function() {
        apply_filters();
    } );
    
    show_main_part( 'nodes' );
    
    var help_text = [
        'Nodes:',
        '<ul>',
        '<li>string   => lookup by the node name</li>',
        '<li><b>t:</b>string => lookup by tag name</li>',
        '</ul>'
    ].join( '\n' );
    
    $( '#filter-help' ).popover( {
        html   : true,
        content: help_text
    } );
    
} );


// Go with all nodes and print them on the list elements
function refresh_nodes() {
    var items = [];
    for ( var i = 0; i < nodes.length; i++ ) {
        var n = nodes[ i ];
        var s = n.generate_host_list_entry();
        items.push( s );
    }
    
    $( "#nodes" ).html( '' );
    
    var ul = $( "<ul/>", {
        "class": "node-list"
    } ).appendTo( "#nodes" );
    
    for ( var i = 0; i < items.length; i++ ) {
        ul.append( items[ i ] );
    }
    
    apply_filters();
    sort_lists();
    update_counts();
    
    var tile_items = [];
    for ( var i = 0; i < nodes.length; i++ ) {
        var n   = nodes[ i ];
        var grp = create_empty_tile( n );
        tile_items.push( grp );
        // add to the layer, it was set to not visible at the creation, and will be set to visible when inserted into a panel
        layer.add( grp );
    }
    fill_panel( node2, tile_items );
    layer.draw();
    console.log( 'FINISH' );
}


function find_node( nuuid ) {
    var node = null;
    $.each( nodes, function( key, val ) {
        if ( val.uuid == nuuid ) {
            node = val;
        }
    } );
    return node;
}


// Detail show be called by a NON modal page
function show_detail( nuuid ) {
    var node = find_node( nuuid );
    if ( node == null ) {
        // no such node
        return;
    }
}


// Clean all detail content from old content
function clean_detail() {
    $( '#detail-header' ).html( '' );
    $( '#detail-checks' ).html( '' );
    $( '#detail-collectors-list' ).html( '' );
    $( '#detail-collectors-data' ).html( '' );
    $( '#detail-detectors' ).html( '' );
    $( '#detail-information' ).html( '' );
    show_detail_part( 'checks' ); // show checks by default
}


// only show a specific detail part (like checks)
function show_detail_part( part ) {
    // first hide all
    $( '#detail .detail-part' ).hide();
    $( '#detail-' + part ).show();
}


function show_collector( col_name ) {
    $( '#collector-data-' + col_name ).show();
}


var __is_panel_open = false;
function toggle_right_panel() {
    if ( __is_panel_open ) {
        close_right_panel();
    }
    else {
        open_right_panel();
    }
}


// Force a close of the right panel
function close_right_panel() {
    // if already close, bail out
    if ( !__is_panel_open ) {
        return;
    }
    __is_panel_open = false;
    $( '#part-right' ).removeClass( 'expanded' );
}


// Force an open of the right panel
function open_right_panel() {
    // if already open, bail out
    if ( __is_panel_open ) {
        return;
    }
    __is_panel_open = true;
    $( '#part-right' ).addClass( 'expanded' );
}


// Ok let's roll and really connect to our main server at soon
// as it is connected :)
$( function() {
    function do_load() {
        if ( server != null ) {
            console.log( 'OK Election is done, we can load' );
            load_nodes();
        }
        else {
            console.log( 'Cannot load, waiting server elecgtion' );
            setTimeout( do_load, 100 );
        }
    }
    
    do_load();
} );


var webso_con = null;


function do_webso_connect() {
    
    // No server to connect to, do nothing a wait a new can be elected
    var icon_connection = $( '#icon-connection' );
    if ( server == null ) {
        icon_connection.addClass( 'red' );
        icon_connection.attr( 'data-original-title', 'Websocket: ✘' ).tooltip( 'fixTitle' );
        elect_server();
        return;
    }
    
    if ( webso_con == null ) {
        var e = pot_servers[ server ];
        console.log( 'Connexion try to websocket' );
        var ws_uri = 'ws://' + e.hostname + ':' + e.ws_port + '/ws';
        console.log( 'Connexion to websocket: ' + ws_uri );
        webso_con = new WebSocket( ws_uri );
        icon_connection.tooltip( { title: 'Connexion to websocket in progress' } );
        webso_con.onopen = function() {
            console.log( 'Connection open!' );
            // We remove the red from the icon so it's back to black
            icon_connection.removeClass( 'red' );
            icon_connection.attr( 'data-original-title', 'Websocket: ✔' ).tooltip( 'fixTitle' );
        };
        
        webso_con.onerror = function() {
            webso_con = null;
            // Put the icon for connection in red
            icon_connection.addClass( 'red' );
            icon_connection.attr( 'data-original-title', 'Websocket: ✘' ).tooltip( 'fixTitle' );
            console.log( 'Websocket connection error to ' + ws_uri );
            server = null;
            // We got a problem, reelect a new server
            elect_server();
        };
        
        webso_con.onclose = function() {
            webso_con = null;
            // Put the icon for connection in red
            icon_connection.addClass( 'red' );
            icon_connection.attr( 'data-original-title', 'Websocket: ✘' ).tooltip( 'fixTitle' );
            console.error( 'Wesocket connection error to ' + ws_uri );
            server = null;
            // A problem? let's look at a new server to load from
            elect_server();
        };
        
        webso_con.onmessage = function( e ) {
            console.log( "Socket message:", e.data );
            // Load the host update as a json dict
            var oraw = JSON.parse( e.data );
            if ( oraw.channel != 'gossip' ) {
                console.log( 'Unmanaged websocket message ' + oraw );
                return;
            }
            
            var o = oraw.payload;
            
            var nuuid = o.uuid;
            
            var n = find_node( nuuid );
            if ( n != null ) {  // was existing
                n.update( o );
            }
            else { // ok a new one
                // Save this host in the list :)
                n = new Node( o );
                nodes.push( n );
            }
            
            // Now generate the doc string from our new host
            var s = n.generate_host_list_entry();
            
            // Delete the previous li for this node
            $( '#' + nuuid ).remove();
            // ok add new the one
            $( s ).appendTo( $( '#nodes > ul' ) );
            // resort and hide if need
            apply_filters();
            sort_lists();
            update_counts();
            // If it was the selected, update the detail panel
            console.debug( 'SELECTED ' + selected + ' AND ' + nuuid );
            if ( nuuid == selected ) {
                n.update_and_show_detail();
            }
        };
    }
}


setInterval( do_webso_connect, 1000 );


$( function() {
    do_webso_connect();
} );


/*************************************************
 EVAL (yes it's bad but soooo good)
 *************************************************/
function get_and_display_eval_result( node, postdata ) {
    var addr        = node.addr;
    var port        = node.port;
    var server_addr = addr + ':' + port;
    var _id         = 'eval-result-' + node.uuid;
    var now         = new Date().getTime();
    $.ajax( {
        type   : "POST",
        url    : 'http://' + server_addr + '/agent/evaluator/eval?_t=' + now,
        data   : postdata,
        success: function( data ) {
            console.log( 'UPDATE _id' + _id );
            $( '#' + _id ).html( data.toString() );
        }
    } );
}

function evaluate_expr() {
    var expr = $( '#evaluations-rule-input' ).val();
    console.log( 'EXPRESSION: ' + expr );
    var expr64 = btoa( expr );
    
    var postdata = { 'expr': expr64 };
    
    
    var eval_result_cont = $( '#evaluations-result' );
    // First clean previous result
    eval_result_cont.html( '' );
    var ul = $( '<ul>' );
    eval_result_cont.append( ul );
    for ( var i = 0; i < nodes.length; i++ ) {
        if ( nodes[ i ].state != 'alive' ) {
            continue;
        }
        var uuid = nodes[ i ].uuid;
        var name = nodes[ i ].name;
        var _id  = 'eval-result-' + uuid;
        var li   = $( '<li >' + name + ':<span id="' + _id + '" >[.... in progress ....]</span></li>' );
        ul.append( li );
    }
    
    for ( var i = 0; i < nodes.length; i++ ) {
        var node = nodes[ i ];
        
        if ( node.state != 'alive' ) {
            continue;
        }
        
        get_and_display_eval_result( node, postdata );
    }
}

function get_available_functions() {
    var now = new Date().getTime();
    // Get available functions from the server
    $.getJSON( 'http://' + server + '/agent/evaluator/list?_t=' + now, function( data ) {
        // first agent information
        var tpl = get_template( 'tpl-evaluations-available-functions' );
        console.log( 'FUNCTIONS' );
        console.log( data );
        for ( var i = 0; i < data.length; i++ ) {
            var e = data[ i ];
            console.log( 'ARG' );
            console.log( e );
            var prototype = e.prototype;
            if ( prototype != null ) {
                var _parts = [];
                for ( var j = 0; j < prototype.length; j++ ) {
                    var p        = prototype[ j ];
                    var arg_name = p[ 0 ];
                    var arg_def  = p[ 1 ];
                    if ( arg_def == '__NO_DEFAULT__' ) {
                        _parts.push( arg_name );
                    }
                    else { // really with default value, set it
                        _parts.push( arg_name + '=' + arg_def );
                    }
                }
                e.prototype_cleaned = _parts;
            }
            else {
                e.prototype_cleaned = null;
            }
            
            var converter = new showdown.Converter();
            var _html     = converter.makeHtml( e.doc );
            e.doc         = _html;
        }
        var s = Mustache.to_html( tpl, { 'functions': data } );
        $( '#evaluations-available-functions' ).html( s );
        
    } );
    
}


/***************************************************************
 *                Executions
 **************************************************************/
var execution_results = {};
var exec_start        = 0;

function get_and_show_result( nuuid, exec_id ) {
    console.log( 'GET RESULT FOR ' + nuuid + ' and exec id' + exec_id );
    $.getJSON( 'http://' + server + '/exec-get/' + exec_id, function( data ) {
        if ( data == null ) {
            return;  // still not finish
        }
        console.log( 'GET RESULT DATA for ' + nuuid );
        console.log( data );
        delete execution_results[ nuuid ];
        $( '#execution-result-' + nuuid ).html( 'RESULT:' + data.output );
    } ); // if error, still missing key
    
}


// now loop to get results
function get_and_show_results() {
    
    console.log( 'EXEC RESULTS' );
    console.log( execution_results );
    
    nb_still_execute = 0;
    for ( var nuuid in execution_results ) {
        if ( execution_results.hasOwnProperty( nuuid ) ) {
            nb_still_execute += 1;
            var exec_id = execution_results[ nuuid ].exec_id;
            console.log( 'GET RESULT FOR ' + nuuid + 'and exec id ' + exec_id );
            get_and_show_result( nuuid, exec_id );
        }
    }
    var now = new Date().getTime();
    // quit after 10s
    if ( (now - exec_start) > 30000 ) {
        console.log( 'EXITING EXECUTION' );
        execution_results = {};
        return;
    }
    // If there is still results, loop more
    if ( nb_still_execute != 0 ) {
        console.log( 'STILL EXEC RESULT, more ' + nb_still_execute );
        setTimeout( get_and_show_results, 1000 );
    }
}


function launch_executions() {
    execution_results = {};
    var tag           = $( '#executions-tag-input' ).val();
    var cmd           = $( '#executions-command-input' ).val();
    console.log( 'EXECUTE COMMANDS:[' + cmd + '] for tag [' + tag + ']' );
    
    // First clean execution container
    var result_cont = $( '#execution-result' );
    result_cont.html( '' );
    exec_start = new Date().getTime();
    $.getJSON( 'http://' + server + '/exec/' + tag + '?cmd=' + cmd + '&_t=' + exec_start, function( data ) {
        console.log( 'GET RESULT FOR exec' );
        console.log( data );
        var nodes_exec = data.nodes;
        
        for ( var i = 0; i < nodes_exec.length; i++ ) {
            var nuuid   = nodes_exec[ i ][ 0 ];
            var exec_id = nodes_exec[ i ][ 1 ];
            var node    = find_node( nuuid );
            // if cannot find it, bail out, not a problem
            if ( node == null ) {
                continue;
            }
            execution_results[ nuuid ] = { 'uuid': nuuid, 'exec_id': exec_id };
            var div                    = $( '<div class="execution-bloc"><div class="execution-name">' + node.name + '</div><div class="execution-result" id="execution-result-' + node.uuid + '" ></div></div>' );
            result_cont.append( div );
        }
        
        
        setTimeout( get_and_show_results, 1000 );
        
    } );
    
}





///////////////// TREEMAP VIEW


var aparencies = [
    {
        radius         : 30,
        XOffset        : 60,
        YOffset        : 55,
        stroke_width   : 3,
        PairVal        : 60,
        ImpairVal      : 30,
        tile_box_size_x: 68,
        tile_box_size_y: 60
    },
    {
        radius         : 15,
        XOffset        : 35,
        YOffset        : 30,
        stroke_width   : 2,
        PairVal        : 45,
        ImpairVal      : 30,
        tile_box_size_x: 36,
        tile_box_size_y: 30
    }
];


///////////// TREEMAP
var node_display_groups = [];
var state,
    layer,
    right_stage,
    right_layer         = null;
var MARGIN              = 10;
var node2               = null;
var root                = null;

var right_tile,
    right_label_char;

var renderer = function( x, y, w, h, n ) {
    console.debug( 'renderer::', x, y, w, h, stage );
    
    if ( n.data ) {
        n.new_x = x;
        n.new_y = y;
        n.new_w = w;
        n.new_h = h;
    }
};

function __get_node_stroke_color( node ) {
    if ( node.state === 'alive' ) {
        stroke_color = '#56D444';  // vert flashy
    }
    if ( node.status === 'warning' ) {
        stroke_color = 'orange';
    }
    if ( node.status === 'leave' ) {
        stroke_color = '#6FB8FD';  // bleu clair
    }
    if ( node.state === 'dead' ) {
        stroke_color = '#D54C46';  // rouge
    }
    return stroke_color;
}


function reset_node_preview() {
    right_tile.attrs.stroke       = '#666666';
    right_tile.attrs.strokeWitdth = 0;
    
    right_label_char.setText( '' );
    right_tile.draw();
    right_label_char.draw();
    right_layer.draw();
}
function update_node_preview( node ) {
    console.log( 'PREVIEW NODE:', node );
    var stroke_color              = __get_node_stroke_color( node );
    right_tile.attrs.stroke       = stroke_color;
    right_tile.attrs.strokeWitdth = 3;
    
    right_label_char.setText( node.name );
    
    right_tile.draw();
    right_label_char.draw();
    right_layer.draw();
}


var print_panel = function( n ) {
    console.log( 'Priting node', n );
    console.log( 'Parent:', n.my_parent, '     n.frame.x:', n.frame.x, '        x+n.parent.frame.x:', n.parent.frame.x );
    
    var n_x      = n.frame.x;
    var n_y      = n.frame.y;
    var n_width  = n.frame.width;
    var n_height = n.frame.height;
    // If parent, remove margin
    if ( n.my_parent ) {
        console.log( 'Remove margin from my parent:', n_x, n.my_parent.pos_x, MARGIN );
        n_x += n.my_parent.pos_x + MARGIN;
        n_y += n.my_parent.pos_y + MARGIN;
        n_width  = n_width - 2 * MARGIN;
        n_height = n_height - 2 * MARGIN;
        console.log( 'RES ', n_x );
    }
    
    n.pos_x      = n_x;
    n.pos_y      = n_y;
    n.pos_width  = n_width;
    n.pos_height = n_height;
    
    var rect = new Kinetic.Rect( {
        x          : 0,
        y          : 0,
        width      : n_width,
        height     : n_height,
        stroke     : "red",
        strokeWidth: 1,
        fill       : n.color
    } );
    
    var label_char = new Kinetic.Text( {
        x        : 0,
        y        : 0,
        text     : n.data,
        fontSize : 20,
        width    : 140,
        align    : 'center',
        fill     : 'black',
        draggable: false
    } );
    
    
    var grp = new Kinetic.Group( {
        x        : n_x,
        y        : n_y,
        draggable: false
    } );
    
    grp.on( 'click', function() {
        console.log( this );
    } );
    
    
    
    grp.on( 'mouseover', function() {
        //this.opacity(0.1);
        //this.attrs.x += 10;
        layer.draw();
    } );
    
    grp.on( 'mouseout', function() {
        //this.opacity(1);
        layer.draw();
        //console.log(this);
    } );
    
    
    grp.add( rect );
    grp.add( label_char );
    
    console.log( 'RECT    color:', n.color, '  name:', n.data, '    n_y:', n_y, '     n_x:', n_x, '     y_height:', n_height, '   x_width:', n_width );
    layer.add( grp );
    n.rect = grp;
};




function create_empty_tile( node ) {
    
    if ( typeof node === 'undefined' ) {
        node = null;
    }
    
    var apar_idx = 1;
    var aparency = aparencies[ apar_idx ];
    
    var radius = aparency.radius;
    // if a place holder, set a radius
    if ( node == null ) {
        radius -= 1;
    }
    else {
        radius += 1;
    }
    var stroke_width = aparency.stroke_width;
    var color        = '#666666'; // noir
    if ( node == null ) {
        var color = '#BBBBBB';
    }
    //'#EBEBEB'; // gray
    var name = '';
    
    var stroke_color = '#6FB8FD';// bleu clair
    if ( node !== null ) {
        stroke_color = __get_node_stroke_color( node );
    }
    
    
    var tile = new Kinetic.RegularPolygon( {
        x        : 0,
        y        : 0,
        sides    : 6,
        radius   : radius,
        fill     : color,
        draggable: false
    } );
    
    if ( node != null ) {
        tile.attrs.stroke        = stroke_color;
        tile.attrs.strokeWidth   = stroke_width;
        tile.attrs.shadowOpacity = 0.1;
    }
    
    
    var grp = new Kinetic.Group( {
        x        : 10,
        y        : 10,
        draggable: false
    } );
    
    grp.__data = { 'node': node };
    
    
    // z_index:
    // * placeholder: 100
    // * real node: 200 (over place holder)
    
    var z_index = 100;
    if ( node != null ) {
        z_index = 200;
    }
    //grp.setZIndex(z_index);
    
    // If a node, don't display it currently, only when need
    if ( node != null ) {
        grp.setVisible( false );
    }
    
    grp.add( tile );
    
    // only add hover and clic on group with a real node on it
    if ( node != null ) {
        grp.on( 'click', function() {
            console.log( 'Click on :', this.__data.node );
            clean_detail();
            this.__data.node.update_and_show_detail();
            open_right_panel();
            update_node_preview( this.__data.node );
        } );
        
        grp.on( 'mouseover', function() {
            console.log( 'GROUP OVER ', this );
            //this.opacity(0.9);
            //this.attrs.scaleX = 2;
            //this.attrs.scaleY = 2;
            // High Z the element when overing it
            //this.setZIndex(99999);
            //this.rotateDeg(0);
            //layer.draw();
            update_node_preview( this.__data.node );
            //this.draw();
        } );
        
        grp.on( 'mouseout', function() {
            //this.opacity(1);
            //this.attrs.scaleX = 1;
            //this.attrs.scaleY = 1;
            //this.rotateDeg(0);
            //layer.draw();
            //console.log(this);
            reset_node_preview( this.__data.node );
        } );
    }
    
    return grp;
}




//   create_hive
function fill_panel( panel, node_tiles ) {
    
    var apar_idx = 1;
    var aparency = aparencies[ apar_idx ];
    var XOffset  = aparency.XOffset;
    var YOffset  = aparency.YOffset;
    
    if ( typeof node_tiles === 'undefined' ) {
        node_tiles = [];
    }
    
    // Size of a tile for rect box size, so we know how much we can put on the screen
    var tile_box_size_x = aparency.tile_box_size_x;
    var tile_box_size_y = aparency.tile_box_size_y;
    
    var panel_width  = panel.pos_width;
    var panel_height = panel.pos_height;
    
    console.debug( 'FILL PANEL ', panel.data, panel_width / tile_box_size_x );
    var mtpl = parseInt( (panel_width - 2 * MARGIN) / tile_box_size_x );
    console.debug( 'mtpl::', mtpl );
    
    var numberLines = parseInt( (panel_height - 2 * MARGIN) / tile_box_size_y );
    
    console.log( 'Tiles: ', mtpl, ' by line.\nNumber of lines:', numberLines, '.\nTotal of tiles:', numberLines * mtpl );
    // Now fill it
    
    // If we are in filling place holder, fill all the lines
    if ( node_tiles.length == 0 ) {
        
        panel.place_holder_tiles = [];
        
        // FILL tile place holders on the panel
        var x_idx = 0;
        // We try to fill the screen
        var y_idx = 1;
        
        while ( y_idx < numberLines + 1 ) {
            // odd/even line are not the same number of tile
            if ( y_idx % 2 === 0 ) {
                var tpl           = mtpl;
                var PairImpairVal = aparency.PairVal;
            }
            else {
                var tpl           = mtpl;
                var PairImpairVal = aparency.ImpairVal;
            }
            while ( x_idx < tpl ) {
                var grp     = create_empty_tile( null );
                var x       = panel.pos_x + x_idx * XOffset + PairImpairVal;
                var y       = panel.pos_y + y_idx * YOffset;
                grp.attrs.x = x;
                grp.attrs.y = y;
                //console.log('SET TO', tnum, x, y_idx, y);
                layer.add( grp );
                panel.place_holder_tiles.push( grp );
                x_idx++;
            }
            x_idx = 0;
            y_idx++;
        }
        //layer.draw();
    }
    else { // only fill nodes that must be
        
        var node_idx = 0;
        
        // FILL tile place holders on the panel
        var x_idx  = 0;
        // We try to fill the screen
        var y_idx  = 1;
        var finish = false;
        while ( y_idx < numberLines + 1 ) {
            
            if ( finish ) {
                break;
            }
            
            // odd/even line are not the same number of tile
            if ( y_idx % 2 === 0 ) {
                var tpl           = mtpl;
                var PairImpairVal = aparency.PairVal;
            }
            else {
                var tpl           = mtpl;
                var PairImpairVal = aparency.ImpairVal;
            }
            while ( x_idx < tpl ) {
                if ( node_idx == node_tiles.length ) {
                    finish = true;
                    break;
                }
                
                var node_grp = node_tiles[ node_idx ];
                // as we insert into a panel, set visible
                node_grp.setVisible( true );
                node_idx += 1;
                
                //var grp = create_empty_tile();
                var x            = panel.pos_x + x_idx * XOffset + PairImpairVal;
                var y            = panel.pos_y + y_idx * YOffset;
                node_grp.attrs.x = x;
                node_grp.attrs.y = y;
                //console.log('SET TO', tnum, x, y_idx, y);
                // TODO: only add once?
                console.log( 'ADD SPECIAL NODE GROUP', node_grp, x_idx, y_idx );
                
                x_idx++;
            }
            x_idx = 0;
            y_idx++;
        }
    }
}



function do_split() {
    
    // First clean all previous panel
    node2.rect.remove();
    for ( var i = 0; i < node2.place_holder_tiles.length; i++ ) {
        var grp = node2.place_holder_tiles[ i ];
        grp.remove();
    }
    node2.place_holder_tiles = [];
    node2.rect               = null;
    
    var node_1 = {
        data     : "NODE 1", weight: 1, x: null, y: null,
        new_x    : null, new_y: null,
        new_w    : null, new_h: null,
        my_parent: root, color: 'white', rect: null
    };
    
    var node_2 = {
        data     : "NODE 2", weight: 1, x: null, y: null,
        new_x    : null, new_y: null,
        new_w    : null, new_h: null,
        my_parent: root, color: 'white', rect: null
    };
    
    var tree = {
        frame: { x: 0, y: 0, width: root.pos_width, height: root.pos_height },
        nodes: [ node_1, node_2 ]
    };
    
    treemap.squarify( tree, renderer );
    
    
    for ( var i = 0; i < tree.nodes.length; i++ ) {
        var n = tree.nodes[ i ];
        //console.log(rect);
        print_panel( n );
    }
    fill_panel( node_1 );
    fill_panel( node_2 );
    
    var tile_items_1 = [];
    var tile_items_2 = [];
    for ( var i = 0; i < nodes.length; i++ ) {
        var n   = nodes[ i ];
        var grp = create_empty_tile( n );
        if ( i % 2 == 0 ) {
            tile_items_1.push( grp );
        }
        else {
            tile_items_2.push( grp );
        }
        // add to the layer, it was set to not visible at the creation, and will be set to visible when inserted into a panel
        layer.add( grp );
    }
    fill_panel( node_1, tile_items_1 );
    fill_panel( node_2, tile_items_2 );
    
    layer.draw();
    
}

$( function() {
    
    
    var WIDTH  = $( '#container' ).width() - 50;
    var HEIGHT = $( '#container' ).height() - 50;
    
    stage = new Kinetic.Stage( {
        container: "container",
        width    : WIDTH,
        height   : HEIGHT
    } );
    
    layer = new Kinetic.Layer();
    
    
    // Right focus
    var right_focus_width  = $( '#right-container' ).width();
    var right_focus_height = $( '#right-container' ).height();
    
    right_stage = new Kinetic.Stage( {
        container: "right-container",
        width    : right_focus_width,
        height   : right_focus_height
    } );
    
    right_layer = new Kinetic.Layer();
    right_stage.add( right_layer );
    right_tile = new Kinetic.RegularPolygon( {
        x        : 90,
        y        : 95,
        sides    : 6,
        radius   : 90,
        fill     : '#666666',
        draggable: false
    } );
    right_layer.add( right_tile );
    right_label_char = new Kinetic.Text( {
        x        : 20,
        y        : 60,
        text     : 'BB',
        fontSize : 20,
        width    : 140,
        align    : 'center',
        fill     : 'white',
        draggable: false
    } );
    right_layer.add( right_label_char );
    right_layer.draw();
    
    stage.add( layer );
    
    root  = { data: "root", my_parent: null, pos_x: MARGIN, pos_y: MARGIN, pos_width: WIDTH, pos_height: HEIGHT, frame: { x: 0, y: 0, width: WIDTH, height: HEIGHT } };
    node2 = {
        data     : "Leaf 2", weight: 0.6, x: null, y: null,
        new_x    : null, new_y: null,
        new_w    : null, new_h: null,
        my_parent: root, color: 'white', rect: null
    };
    
    var tree = {
        frame: { x: 0, y: 0, width: WIDTH, height: HEIGHT },
        nodes: [
            node2
        ]
    };
    
    treemap.squarify( tree, renderer );
    
    
    
    
    for ( var i = 0; i < tree.nodes.length; i++ ) {
        var n = tree.nodes[ i ];
        //console.log(rect);
        print_panel( n );
    }
    fill_panel( node2 );
    
    layer.draw();
    
    /*
     var node6 = {
     data     : "Leaf 6", weight: 0.6, x: null, y: null,
     new_x    : null, new_y: null,
     new_w    : null, new_h: null,
     my_parent: node1, color: 'green', rect: null
     };
     */
    
    /*
     var tree_in_1 = {
     //frame: {x:0,y:0, width:node1.frame.width, height:node1.frame.height},
     frame: { x: 0, y: 0, width: node1.pos_width, height: node1.pos_height },
     nodes: [
     node6
     ]
     };
     
     
     treemap.squarify( tree_in_1, renderer );
     for ( var i = 0; i < tree_in_1.nodes.length; i++ ) {
     var n = tree_in_1.nodes[ i ];
     console.log( 'Printing tree_in_1::', n );
     print_panel( n );
     }
     
     
     layer.draw();
     */
    
    /*
     var tween = new Kinetic.Tween({
     node: this,
     duration: 0.2,
     x: 200,
     y: 100,
     }).play();
     */
    
} );

