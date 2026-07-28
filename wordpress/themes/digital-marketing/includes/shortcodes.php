<?php

if (!function_exists('register_button')) {
function register_button( $buttons ) {
   array_push( $buttons, "|", "qode_shortcodes" );
   return $buttons;
}
}

if (!function_exists('add_plugin')) {
function add_plugin( $plugin_array ) {
   $plugin_array['qode_shortcodes'] = get_template_directory_uri() . '/includes/qode_shortcodes.js';
   return $plugin_array;
}
}

if (!function_exists('qode_shortcodes_button')) {
function qode_shortcodes_button() {

   if ( ! current_user_can('edit_posts') && ! current_user_can('edit_pages') ) {
      return;
   }

   if ( get_user_option('rich_editing') == 'true' ) {
      add_filter( 'mce_external_plugins', 'add_plugin' );
      add_filter( 'mce_buttons', 'register_button' );
   }

}
}

add_action('init', 'qode_shortcodes_button');


if (!function_exists('no_wpautop')) {
function no_wpautop($content) 
{ 
        $content = do_shortcode( shortcode_unautop($content) ); 
        $content = preg_replace( '#^<\/p>|^<br \/>|<p>$#', '', $content );
        return $content;
}
}
if (!function_exists('num_shortcodes')) {
function num_shortcodes($content) 
{ 
        $columns = substr_count( $content, '[pricing_cell' );
		return $columns;
}
}

/* Three columns wrap shortcode */

if (!function_exists('three_columns')) {
function three_columns($atts, $content = null) {
    return '<div class="three_columns clearfix">' . do_shortcode($content) . '</div>';
}
}
add_shortcode('three_columns', 'three_columns');

/* Four columns wrap shortcode */

if (!function_exists('four_columns')) {
function four_columns($atts, $content = null) {
    return '<div class="four_columns clearfix">' . do_shortcode($content) . '</div>';
}
}
add_shortcode('four_columns', 'four_columns');

/* Two columns wrap shortcode */

if (!function_exists('two_columns')) {
function two_columns($atts, $content = null) {
    return '<div class="two_columns_50_50 clearfix">' . do_shortcode($content) . '</div>';
}
}
add_shortcode('two_columns', 'two_columns');

/* Two columns 66_33 wrap shortcode */

if (!function_exists('two_columns_66_33')) {
function two_columns_66_33($atts, $content = null) {
    return '<div class="two_columns_66_33 clearfix">' . do_shortcode($content) . '</div>';
}
}
add_shortcode('two_columns_66_33', 'two_columns_66_33');

/* Two columns 33_66 wrap shortcode */

if (!function_exists('two_columns_33_66')) {
function two_columns_33_66($atts, $content = null) {
    return '<div class="two_columns_33_66 clearfix">' . do_shortcode($content) . '</div>';
}
}
add_shortcode('two_columns_33_66', 'two_columns_33_66');

/* Two columns 75_25 wrap shortcode */

if (!function_exists('two_columns_75_25')) {
function two_columns_75_25($atts, $content = null) {
    return '<div class="two_columns_75_25 clearfix">' . do_shortcode($content) . '</div>';
}
}
add_shortcode('two_columns_75_25', 'two_columns_75_25');

/* Two columns 25_75 wrap shortcode */

if (!function_exists('two_columns_25_75')) {
function two_columns_25_75($atts, $content = null) {
    return '<div class="two_columns_25_75 clearfix">' . do_shortcode($content) . '</div>';
}
}
add_shortcode('two_columns_25_75', 'two_columns_25_75');

/* Column one shortcode */

if (!function_exists('column1')) {
function column1($atts, $content = null) {
	return '<div class="column1"><div class="column_inner">' . do_shortcode($content) . '</div></div>';
}
}
add_shortcode('column1', 'column1');

/* Column two shortcode */

if (!function_exists('column2')) {
function column2($atts, $content = null) {
	return '<div class="column2"><div class="column_inner">' . do_shortcode($content) . '</div></div>';
}
}
add_shortcode('column2', 'column2');

/* Column three shortcode */

if (!function_exists('column3')) {
function column3($atts, $content = null) {
   return '<div class="column3"><div class="column_inner">' . do_shortcode($content) . '</div></div>';
}
}
add_shortcode('column3', 'column3');

/* Column four shortcode */

if (!function_exists('column4')) {
function column4($atts, $content = null) {
   return '<div class="column4"><div class="column_inner">' . do_shortcode($content) . '</div></div>';
}
}
add_shortcode('column4', 'column4');

/* Dropcaps shortcode */

if (!function_exists('dropcaps')) {
function dropcaps($atts, $content = null) {
	extract(shortcode_atts(array("style" => ""), $atts));
	return "<span class='dropcap $style'>" . no_wpautop($content)  . "</span>";
}
}
add_shortcode('dropcaps', 'dropcaps');

/* Blockquote shortcode */

if (!function_exists('blockquote')) {
function blockquote($atts, $content = null) {
	$html = ""; 
  extract(shortcode_atts(array("width" => ""), $atts));
	$html .= "<blockquote"; 
	if($width > 0){
		$html .= " style=width:$width%;";
	}
	$html .= ">" . no_wpautop($content) . "</blockquote>";
  return $html;
}
}
add_shortcode('blockquote', 'blockquote');

/* Message shortcode */

if (!function_exists('message')) {
function message($atts, $content = null) {
	global $qode_options_lounge;
  $html = ""; 
	extract(shortcode_atts(array("background_color"=>""), $atts));
	$html .= "<div class='message";
	$html .= "' style='";
	if($background_color != ""){
		$html .= 'background-color: '.$background_color.'; ';
	}
	
	$html .= "'><a href='#' class='close'></a>" .no_wpautop($content) . "</div>";
	
	return $html;
}
}
add_shortcode('message', 'message');

/* Accordion shortcode */

if (!function_exists('accordion')) {
function accordion($atts, $content = null) {
	extract(shortcode_atts(array("accordion_type" => ""), $atts));
	return "<div class='accordion $accordion_type'>" . no_wpautop($content) . "</div>";
}
}
add_shortcode('accordion', 'accordion');

/* Accordion item shortcode */

if (!function_exists('accordion_item')) {
function accordion_item($atts, $content = null) {

	extract(shortcode_atts(array("caption" => ""), $atts));
	return "<h3><span><span class='control-pm'></span></span>".$caption."</h3><div class='accordion_content'><div class='accordion_content_inner'>" . no_wpautop($content) . "</div></div>";
}
}
add_shortcode('accordion_item', 'accordion_item');

/* Unordered List shortcode */

if (!function_exists('unordered_list')) {
function unordered_list($atts, $content = null) {
    extract(shortcode_atts(array("style" => ""), $atts));
    $html =  "<div class='list $style'>" . $content . "</div>";  
    return $html;
}
}
add_shortcode('unordered_list', 'unordered_list');

/* Ordered List shortcode */

if (!function_exists('ordered_list')) {
function ordered_list($atts, $content = null) {
    $html =  "<div class=ordered>" . $content . "</div>";  
    return $html;
}
}
add_shortcode('ordered_list', 'ordered_list');

/* Buttons shortcode */

if (!function_exists('button')) {
function button($atts, $content = null) {
	global $qode_options_lounge;
	$html = "";
	extract(shortcode_atts(array("size" => "", "color"=> "", "background_color"=>"", "border_color" => "", "font_size"=>"", "line_height"=>"", "font_style"=>"", "font_weight"=>"", "text"=> "Button", "link"=> "http://qodeinteractive.com/", "target"=> "_self"), $atts));
    $html .=  '<a href="'.$link.'" target="'.$target.'" class="button '.$size.'" style="';
		if($color != ""){
			$html .= 'color: '.$color.'; ';
		}
		if($background_color != ""){
			$html .= 'background-color: '.$background_color.'; ';
		}
		if($border_color != ""){
			$html .= 'border-color: '.$border_color.'; ';
		}
		if($font_size != ""){
			$html .= 'font-size: '.$font_size.'px; ';
		}
		if($line_height != ""){
			$html .= 'line-height: '.$line_height.'px; ';
		}
		if($font_style != ""){
			$html .= 'font-style: '.$font_style.'; ';
		}
		if($font_weight != ""){
			$html .= 'font-weight: '.$font_weight.'; ';
		}
		$html .= '">' . $text . '</a>';  
    return $html;
}
}
add_shortcode('button', 'button');

/* Tabs shortcode */

if (!function_exists('tabs')) {
function tabs( $atts, $content = null ) {
  $html = ""; 
	extract(shortcode_atts(array(
    ), $atts));
	$html .= '<div class="tabs '.(isset($atts['type'])?$atts['type']:'').'">';
	$html .= '<ul class="tabs-nav">';
	$key = array_search((isset($atts['type'])?$atts['type']:''),$atts);
		if($key!==false){
			unset($atts[$key]);
	}
	foreach ($atts as $key => $tab) {
		$html .= '<li><a href="#' . $key . '">' . $tab . '</a></li>';
	}
	$html .= '</ul>';
	$html .= '<div class="tabs-container">';
	$html .= no_wpautop($content) .'</div></div>';
	return $html;
}
}
add_shortcode('tabs', 'tabs');

/* Tab shortcode */

if (!function_exists('tab')) {
function tab( $atts, $content = null ) {
  $html = ""; 
	extract(shortcode_atts(array(
    ), $atts));
	$html .= '<div id="tab' . $atts['id'] . '" class="tab-content">' . no_wpautop($content) .'</div>';
	return $html;
}
}
add_shortcode('tab', 'tab');

/* Progress bars shortcode */

if (!function_exists('progress_bars')) {
function progress_bars($atts, $content = null) {
	extract(shortcode_atts(array(), $atts));
    $html =  "<div class='progress_bars'>" . no_wpautop($content) . "</div>";  
    return $html;
}
}
add_shortcode('progress_bars', 'progress_bars');

/* Progress bar shortcode */

if (!function_exists('progress_bar')) {
function progress_bar($atts, $content = null) {
	extract(shortcode_atts(array("title" => "Web Design", "percent"=> "100"), $atts));
    $html =  "<div class='progress_bar'><span class='progress_title'><h3>$title</h3></span><span class='progress_number'><em></em></span>	<div class='progress_content_outer'><div data-percentage='$percent' class='progress_content'></div></div></div>";  
    return $html;
}
}
add_shortcode('progress_bar', 'progress_bar');

/* Pricing table shortcode */

if (!function_exists('pricing_table')) {
function pricing_table($atts, $content = null) {
  $html = ""; 
	extract(shortcode_atts(array(), $atts));
    	$html .=  "<div class='price_tables";
		$html .= " clearfix'>" . no_wpautop($content) . "</div>";  
    return $html;
}
}
add_shortcode('pricing_table', 'pricing_table');

/* Pricing table column shortcode */

if (!function_exists('pricing_column')) {
function pricing_column($atts, $content = null) {
  $html = ""; 
	extract(shortcode_atts(array("type" => "", "title" => '', "price" => "0", "price_value" => "$", "price_period" => "mo", "link" => "", "button_text" => "Buy Now", "active"=>"" , "active_text"=>"Most Popular"), $atts));
	$html .=  "<div class='price_table'><div class='price_table_inner $type'>";
	if($active == "yes"){
		$html .= "<div class='active_best_price'><p>".$active_text."</p></div>";
	}
	$html .= "<ul><li class='$type'><h3>$title</h3><div class='price_in_table'><sup class='value'>".$price_value."</sup><span class='price'>".$price."</span><sub class='mark'>/".$price_period."</sub></div></li>" . no_wpautop($content) . "<li><div class='button_price_holder'><a class='button medium $type' href='$link'>$button_text</a></div></li></ul></div></div>";
	
    return $html;
}
}
add_shortcode('pricing_column', 'pricing_column');


/* Pricing table cell shortcode */

if (!function_exists('pricing_cell')) {
function pricing_cell($atts, $content = null) {
	extract(shortcode_atts(array(), $atts));
    $html =  "<li class='cell'>" . no_wpautop($content) . "</li>"; 
	return $html;
}
}
add_shortcode('pricing_cell', 'pricing_cell');

/* Testimonials shortcode */

if (!function_exists('testimonials')) {
function testimonials($atts, $content = null) {
	extract(shortcode_atts(array("background_color" => ""), $atts));
  	$html = ""; 	
		$html .=  "<div class='testimonial' style='background-color: $background_color;'><ul class='testimonials'>" . no_wpautop($content) . "</ul></div>";
											
    return $html;
}
}
add_shortcode('testimonials', 'testimonials');

/* Testimonial shortcode */

if (!function_exists('testimonial')) {
function testimonial($atts, $content = null) {
  $html = ""; 
	extract(shortcode_atts(array("name" => "", "border" => ""), $atts));
  	$html .= "<li><h3>$name</h3><p>".no_wpautop($content)."</p>";
  	if($border == "yes"){
  		$html .= "<span class='separator_small'></span>";
  	}
  	"</li>";  
    return $html;
}
}
add_shortcode('testimonial', 'testimonial');

/* Table shortcode */

if (!function_exists('table')) {
function table($atts, $content = null) {
  $html = ""; 
	extract(shortcode_atts(array("border"=>"yes"), $atts));
    $html .=  "<table class='standard-table";
		if($border == "yes"){
			$html .= ' border';
		}
		$html .= "'><tbody>" . no_wpautop($content) . "</tbody></table>";  
    return $html;
}
}
add_shortcode('table', 'table');

/* Table row shortcode */

if (!function_exists('table_row')) {
function table_row($atts, $content = null) {
	extract(shortcode_atts(array(), $atts));
    $html =  "<tr>" . no_wpautop($content) . "</tr>";  
    return $html;
}
}
add_shortcode('table_row', 'table_row');

/* Table head cell shortcode */

if (!function_exists('table_cell_head')) {
function table_cell_head($atts, $content = null) {
	extract(shortcode_atts(array(), $atts));
    $html =  "<th><h3>" . no_wpautop($content) . "</h3></th>";  
    return $html;
}
}
add_shortcode('table_cell_head', 'table_cell_head');

/* Table body cell shortcode */

if (!function_exists('table_cell_body')) {
function table_cell_body($atts, $content = null) {
	extract(shortcode_atts(array(), $atts));
    $html =  "<td>" . no_wpautop($content) . "</td>";  
    return $html;
}
}
add_shortcode('table_cell_body', 'table_cell_body');

/* Highlights shortcode */

if (!function_exists('highlight')) {
function highlight($atts, $content = null) {
	$html =  "<span class='highlight'>" . $content . "</span>";  
    return $html;
}
}
add_shortcode('highlight', 'highlight');

/* H2 With Line shortcode */

if (!function_exists('h2_with_line')) {
function h2_with_line($atts, $content = null) {
	$html =  "<h2 class='title_with_line'>" . $content . "</h2><div class='title_with_line_separator'></div>";  
    return $html;
}
}
add_shortcode('h2_with_line', 'h2_with_line');


/* Action shortcode */

if (!function_exists('action')) {
function action($atts, $content = null) {
	extract(shortcode_atts(array("title" => "New stylish minimalist Wordpress theme avaliable for only $45!"), $atts));
	$html =  "<div class='action'><h2>$title</h2><p>" . no_wpautop($content) . "</p></div>";  
    return $html;
}
}
add_shortcode('action', 'action');

/* Portfolio shortcode */

if (!function_exists('portfolio_list')) {
function portfolio_list($atts, $content = null) {
	$html = "";
	extract(shortcode_atts(array("type" => "1", "columns" => "3", "order_by" => "menu_order" , "order" => "ASC" , "number"=>"-1", "filter"=>'no', "category"=>"", "selected_projects"=>""), $atts));
	
	if($filter == "yes"){
		$html .= "<div class='filter'>
						<span>". __('Filter','qode') ." &nbsp;&nbsp;&nbsp;></span>
						<ul>
						<li><a data-filter='*' href='#'>". __('All','qode') ."</a></li>";
				if ($category == "") {
					$args = array(
						'parent'  => 0
					);
					$portfolio_categories = get_terms( 'portfolio_category',$args);
				} else {
					$top_category = get_term_by('slug',$category,'portfolio_category');
					$term_id = '';
					if (isset($top_category->term_id)) $term_id = $top_category->term_id;
					$args = array(
						'parent'  => $term_id
					);
					$portfolio_categories = get_terms( 'portfolio_category',$args);
				}
				foreach($portfolio_categories as $portfolio_category) {
					$html .=	"<li><a data-filter='.$portfolio_category->slug' href='#'>$portfolio_category->name</a>";
					$args = array(
						'child_of' => $portfolio_category->term_id
					);
					$portfolio_categories2 = get_terms( 'portfolio_category',$args);
					
					if(count($portfolio_categories2) > 0){
						$html .= '<ul>';
						foreach($portfolio_categories2 as $portfolio_category2) {
							$html .=	"<li><a data-filter='.$portfolio_category2->slug' href='#'>$portfolio_category2->name</a></li>";
						}
						$html .= '</ul>';
					}
					
					$html .= '</li>';
				}
		$html .= "</ul></div>";
	}
	$html .= "<div class='portfolio_outer'><div class='portfolio_holder portfolio_holder_v$columns'>";
	
	if ($category == "") {
		$args = array(
			'post_type'=> 'portfolio_page',
			'orderby' => $order_by,
			'order' => $order,
			'posts_per_page' => $number
		);
	} else {
		$args = array(
			'post_type'=> 'portfolio_page',
			'portfolio_category' => $category,
			'orderby' => $order_by,
			'order' => $order,
			'posts_per_page' => $number
		);
	}
	$project_ids = null;
	if ($selected_projects != "") {
		$project_ids = explode(",",$selected_projects);
		$args['post__in'] = $project_ids;
	}
	query_posts( $args );
	if ( have_posts() ) : while ( have_posts() ) : the_post(); 
	$terms = wp_get_post_terms(get_the_ID(),'portfolio_category');
	$html .= "<article class='element ";
	foreach($terms as $term) {
		$html .= "$term->slug ";
	}
	$html .="'>";
	$html .= "<div class='portfolio_article_inner'><div class='image'>".get_the_post_thumbnail()."</div>";
	$html .= "<div class='portfolio_hover'><div class='portfolio_hover_overlay'></div>";
	$html .= "<a href='". get_permalink() ."' class='more'><span class='text_holder'>";
	$html .= "<span class='portfolio_title'>" . get_the_title() . "</span><hr />";
	$html .= '<p>';
		$k=1;
		foreach($terms as $term) {
			$html .= "$term->name";
			if(count($terms) != $k){
				$html .= ', ';
			}
		$k++;
		}
	$html .= '</p>';
	$html .= "</span></a>";
	$html .= "</div></div>";
	if($type == 2) {
		
	$html .= "<div class='portfolio_t2_text_holder'><h3>" . get_the_title() . "</h3>";
	$html .= "<p>" . strip_tags( get_the_excerpt() ) . "</p></div>";
	}
	
	
	
	$html .= "</article>";
						
	endwhile; else: ?>
	<p><?php _e('Sorry, no posts matched your criteria.','qode'); ?></p>
	<?php endif; 	
	wp_reset_query();	
	
	$html .= "</div></div>";
    return $html;
}
}
add_shortcode('portfolio_list', 'portfolio_list');

/* Portfolio slider */

if (!function_exists('portfolio_slider')) {
function portfolio_slider($atts, $content = null) {
	global $wp_query; 
	$html = "";
	extract(shortcode_atts(array("type" => "1", "number"=>"-1", "category"=>"", "selected_projects"=>""), $atts));
	
		if ($category == "") {
		$args = array(
			'post_type'=> 'portfolio_page',
			'orderby' => 'menu_order',
			'order' => 'ASC',
			'posts_per_page' => $number
		);
	} else {
		$args = array(
			'post_type'=> 'portfolio_page',
			'portfolio_category' => $category,
			'orderby' => 'menu_order',
			'order' => 'ASC',
			'posts_per_page' => $number
		);
	}
	$project_ids = null;
	if ($selected_projects != "") {
		$project_ids = explode(",",$selected_projects);
		$args['post__in'] = $project_ids;
	}
	
	query_posts( $args );
	
	
	$html .= '<div class="slider_small type1';
	if($wp_query->post_count < 5) {
		$html .= ' hide_arrows turn_off';
	} else {
		$html .= ' turn_on';
	}
	
	$html .= '"><div class="slider_small_holder"><div class="slider_small_holder_inner"><ul class="slider">';

	if ( have_posts() ) : while ( have_posts() ) : the_post(); 
	$html .= '<li><div class="slide_item">';
	$html .= "<div class='image'>";
	$html .= "<div class='slider_small_hover'><div class='slider_small_hover_overlay'></div>";
	$html .= "<a href='". get_permalink() ."' class='more'><span class='slider_small_text_holder'>";
	$html .= "<span class='slider_small_title'>" . get_the_title() . "</span><hr />";
	$html .= '<p>';
		$k=1;
		$terms = wp_get_post_terms(get_the_ID(),'portfolio_category');
		foreach($terms as $term) {
			$html .= "$term->name";
			if(count($terms) != $k){
				$html .= ', ';
			}
		$k++;
		}
	$html .= '</p>';
	$html .= "</span></a>";
	$html .= "</div>";
	$html .= "<a href='". get_permalink() ."'>".get_the_post_thumbnail()."</a></div>";
		if($type == 2) {
			$html .= "<h3><a href='". get_permalink() . "'>" . get_the_title() . "</a></h3>";
			$html .= "<p>" . strip_tags( get_the_excerpt() ) . "</p>";
		}
	$html .= "</div></li>";
	
	endwhile;
		$html .= "</ul>";
	else: ?>
	<p><?php _e('Sorry, no posts matched your criteria.','qode'); ?></p>
	<?php endif; 	
	wp_reset_query();	
	
	$html .= "</div></div></div>";
    return $html;
}
}
add_shortcode('portfolio_slider', 'portfolio_slider');


/* Sliders shortcode */

if (!function_exists('slider')) {
function slider($atts, $content = null) {
	extract(shortcode_atts(array("type"=>"flex1","id" => "", "min_height"=>""), $atts));
	$page_id = get_the_ID();
	
	$sliders = get_post_meta($page_id, "qode_sliders", true);
		
	$html = "";
	if($type == "flex1" || $type == "flex2"){
		foreach($sliders as $slider) 
		{
		
			if($slider['unique'] == $id) 
			{
				$html .= '<div class="flexslider"';
				if($min_height != ""){
					$html .= ' style="min-height:' . $min_height . 'px;"';
				}
				$html .= '><ul class="slides">';
				$i=0;
				if (count($slider)>1) {
					unset($slider['unique']);
					usort($slider, "compareSlides");
				}
				while (isset($slider[$i]))
				{
						
				
					$slide = $slider[$i];
					
					$href = $slide['link'];
					//$baseurl = site_url();
					$baseurl = home_url();
					$baseurl = str_replace('http://', '', $baseurl);
					$baseurl = str_replace('www', '', $baseurl);
					$host = parse_url($href, PHP_URL_HOST);
					if($host != $baseurl) {
						$target = 'target="_blank"';
					}
					else {
						$target = 'target="_self"';
					}
					
					$html .= '<li class="slide ' . (isset($slide['imgsize'])?$slide['imgsize']:'') . '">';
					$html .= '<div class="image"><img src="' . $slide['img'] . '" alt="' . $slide['title'] . '" /></div>';
					
					if($type == "flex1"){
					
						$html .= '<div class="text ' . $slide['descposition'] . '">';
						if((isset($slide['toplabel'])?$slide['toplabel']:"") != ""){
							$html .= '<span class="toplabel"';
							if($slide['titlecolor'] != ""){
								$html .= ' style="color:'. $slide['titlecolor'] .'"';
							}
							$html .= '>'. $slide['toplabel'] .'</span>';
						}
						if($slide['title'] != ""){
							$html .= '<h2';						
							if($slide['titlecolor'] != ""){
							$html .= ' style="color:'. $slide['titlecolor'] .'"';
							}
							$html .= '>'.$slide['title'].'</h2>';
						}
						$html .= '<p';
						if($slide['color'] != ""){
						$html .= ' style="color:'. $slide['color'] .'"';
						}
						$html .= '>' . $slide['description'] . '</p>';
						if($slide['link'] != ""){
						$html .=	'<a class="button small" ';
							if($slide['linkcolor'] != ""){
							$html .= ' style="color:'. $slide['linkcolor'] .'"';
							}
							$html .= ' href="' . $slide['link'] . '" '. $target .' >';
							if($slide['linklabel'] == ""){
								$html .= __('Read','qode');
							}else{
								$html .= $slide['linklabel'];
							}
							$html .= '</a>';
						}
						$html .= '</div>';
					
					} elseif($type == "flex2"){
						
						$html .= '<div class="text type2">';
						if($slide['title'] != ""){
							$html .= '<h2';						
							if($slide['titlecolor'] != ""){
							$html .= ' style="color:'. $slide['titlecolor'] .'"';
							}
							$html .= '>';
							if($slide['link'] != ""){
								$html .=	'<a';
								if($slide['titlecolor'] != ""){
									$html .= ' style="color:'. $slide['titlecolor'] .'"';
								}
								$html .= ' href="' . $slide['link'] . '" '. $target .' >';
							}
							$html .= $slide['title'].'</a></h2></div>';
						}
					}
					
					$html .= '</li>';
					$i++; 
				}
				$html .= '</ul></div>';
			}							
		}
	}

	if($type == "small"){
		foreach($sliders as $slider) 
		{
		
			if($slider['unique'] == $id){

				$html .= '<div class="slider_small type1';

				$number = count($slider) - 1;
				if($number < 5){
					$html .= ' hide_arrows turn_off';
				} else {
					$html .= ' turn_on';
				}
				
				$html .= '"><div class="slider_small_holder"><div class="slider_small_holder_inner"><ul class="slider">';
				
				$i=0;
				while (isset($slider[$i]))
				{
					$slide = $slider[$i];
					
					$href = $slide['link'];
					$baseurl = home_url();
					$baseurl = str_replace('http://', '', $baseurl);
					$baseurl = str_replace('www', '', $baseurl);
					$host = parse_url($href, PHP_URL_HOST);
					if($host != $baseurl) {
						$target = 'target="_blank"';
					}
					else {
						$target = 'target="_self"';
					}
					$html .= '<li><div class="slide_item">';
					$html .= '<div class="image"><a href="' . $slide['link'] . '" '. $target .'"><img src="' . $slide['img'] . '" alt="' . $slide['title'] . '" /></a></div>';
					$html .= '<h3><a href="' . $slide['link'] . '" '. $target .'">' . $slide['title'] . '</a></h3>';
					$html .= '<p>' . $slide['description'] . '</p>';
				
					
					$html .= '</div></li>';
					$i++; 
				}
				$html .= '</ul></div></div></div>';
				
			}							
		}
	}
	
	return $html;
}
}
add_shortcode('slider', 'slider');


if (!function_exists('parallax')) {
function parallax($atts, $content = null) {
	extract(shortcode_atts(array("pager" => "no",), $atts));
	$html = "";
	$html .= "<section class='parallax'>";
	if($pager == "yes"){
		$html .= '<div class="link_holder_parallax"></div>';
	}
	$html .= no_wpautop($content);
	$html .= "</section>";
	return $html;
}
}
add_shortcode('parallax', 'parallax');

if (!function_exists('parallax_section')) {
function parallax_section($atts, $content = null) {
	extract(shortcode_atts(array("id" => "", "height"=>"300", "title" => "..."), $atts));
	$parallaxes = get_post_meta(get_the_ID(), "qode_parallaxes", true);
	$html = "";
	
	foreach($parallaxes as $parallax) 
	{	
		if($parallax['imageid'] == $id) 
			{
			$html .= '<section id="'.$parallax['imageid'].'" style="background-image:url('. $parallax['parimg'] .'); background-color:'. $parallax['parcolor'] .';" data-height="' . $height . '" data-title="' . $title . '">';
			$html .= '<div class="parallax_content">';
			$html .= no_wpautop($content);
			$html .= '</div>';
			$html .= '</section>';
		}			
	}
	
	return $html;
}
}
add_shortcode('parallax_section', 'parallax_section');


if (!function_exists('separator')) {
function separator($atts, $content = null) {
    extract(shortcode_atts(array("color" => "", "thickness" => "", "up" => "","down" => ""), $atts));
		$html =  '<div style="';
		if($up != ""){
		$html .= "margin-top:". $up ."px;";
		}
		if($down != ""){
		$html .= "margin-bottom:". $down ."px;"; 
		}
		if($color != ""){
		$html .= "background-color: ". $color .";";
		}
		if($thickness != ""){
		$html .= "height:". $thickness ."px;";
		}
		$html .= '" class="separator"></div>';  
		
    return $html;
}
}
add_shortcode('separator', 'separator');

if (!function_exists('separator_small')) {
function separator_small($atts, $content = null) {
    extract(shortcode_atts(array("separator_width" => "", "thickness" => "", "up" => "","down" => ""), $atts));
		$html =  '<div style="';
		if($up != ""){
		$html .= "margin-top:". $up ."px;";
		}
		if($down != ""){
		$html .= "margin-bottom:". $down ."px;"; 
		}
		if($separator_width != ""){
		$html .= "width: ". $separator_width ."px;";
		}
		if($thickness != ""){
		$html .= "height:". $thickness ."px;";
		}
		$html .= '" class="separator_small"></div>';  
		
    return $html;
}
}
add_shortcode('separator_small', 'separator_small');

/* Social Icons shortcode */

if (!function_exists('social_icons')) {
function social_icons($atts, $content = null) {
    extract(shortcode_atts(array("style" => ""), $atts));
    $html = ""; 
    $html .=  "       <ul class='social_menu $style'>";  
    $social_icons_array = explode(",", $content);
    for ($i = 0 ; $i < count($social_icons_array) ; $i = $i + 2)
    {
		$html .=  "<li class='" . trim($social_icons_array[$i]) . "'><a href='" . trim($social_icons_array[$i + 1]) . "' target='_blank'><span class='inner'>" . trim($social_icons_array[$i]) . "</span></a></li>";   
    }
     $html .=  "           </ul>";


    return $html;
}
}
add_shortcode('social_icons', 'social_icons');

/* Services shortcode */

if (!function_exists('service')) {
function service($atts, $content = null) {
    $html = ""; 
	extract(shortcode_atts(array("type"=>"top", "title" => "", "link" => "") , $atts));	
	$html .= '<div class="circle_item circle_'.$type.'">';
	if ($link == "")
		$html .= '<div class="circle"><div style="padding: 70.5px 0px;">'.$title.'</div></div><div class="text">';
	else
		$html .= '<div class="circle"><div style="padding: 70.5px 0px;"><a href="'.$link.'">'.$title.'</a></div></div><div class="text">';
	$html .= no_wpautop($content);
	$html .= '</div></div>';
	
	return $html;
}
}
add_shortcode('service', 'service');


/* Video shortcode */

if (!function_exists('video')) {
function video($atts, $content = null) {
    $html = ""; 
	extract(shortcode_atts(array("type"=>"youtube", "id"=>"", "width"=>"", "height"=>"") , $atts));	
	$html .= "<div class='video_holder'>"; 
	if($type == 'youtube'){
		$html .= '<iframe title="YouTube video player" width="' . $width . '" height="' . $height . '" src="https://www.youtube.com/embed/' . $id . '?wmode=transparent" wmode="Opaque" frameborder="0" allowfullscreen></iframe>';
	}elseif($type == 'vimeo'){
		$html .= '<iframe src="https://player.vimeo.com/video/' . $id . '" width="' . $width . '" height="' . $height . '" frameborder="0"></iframe>';
	}
	$html .= "</div>";
	return $html;
}
}
add_shortcode('video', 'video');

/* Latest post shortcode */

if (!function_exists('latest_post')) {
function latest_post($atts, $content = null) {
	global $qode_options_magnet;
  	$html = ""; 
		extract(shortcode_atts(array("post_number"=>"", "text_length"=>"", "category" => ""), $atts));
		if(empty($post_number)){
		 $post_number = 2;
		}
		if(empty($text_length)){
		 $text_length = 55;
		}
		$q = new WP_Query( 
		   array( 'orderby' => 'date', 'posts_per_page' => $post_number, 'category_name' => $category) 
		);		
		$html .= "<div class='latest_post_holder'>";
		$html .= '<ul class="latest_post">';

			while($q->have_posts()) : $q->the_post();

			$html .= '<li><div class="post_image"><a href="'. get_permalink() .'">' . get_the_post_thumbnail(get_the_id(),'latest_posts') . '</a></div><div class="post_content"><h3><a href="' . get_permalink() . '">' . get_the_title() . '</a></h3>' . '<p>' . substr(get_the_excerpt(), 0, intval($text_length)) . '</p><h6><a href="'. get_permalink() .'">Read more</a></h6></div><div class="latest_post_separator"></div></li>';
			endwhile;

			wp_reset_query();

	return $html . '</ul>' . "</div>";	
}
}
add_shortcode('latest_post', 'latest_post');

/* Icons shortcode */

if (!function_exists('icon')) {
function icon($atts, $content = null) {
    extract(shortcode_atts(array("icon_type" => "", "icon_position" => "", "icon_number" => "", "link" => "", "target" => ""), $atts));
    $html = "";
	if($link != ""){
		if($target == ""){
			$target = "_self";
		}
		$html .=  '<div class="box_small_holder '.$icon_type.' '.$icon_position.'"><a href="'.$link.'" target="'.$target.'"><span class="box_small"><span class="icon '.$icon_type.' icon'.$icon_number.'"></span></span></a></div>';
	} else {
		$html .=  '<div class="box_small_holder '.$icon_type.' '.$icon_position.'"><div class="box_small"><div class="icon '.$icon_type.' icon'.$icon_number.'"></div></div></div>';
	}

    return $html;
}
}
add_shortcode('icon', 'icon');

/* Counter shortcode */

if (!function_exists('counter')) {
function counter($atts, $content = null) {
		extract(shortcode_atts(array("digit" => "", "font_size" => ""), $atts));
    $html = "";  
		$html .=  '<span class="counter" ';
		if($font_size){
			$html .= 'style="font-size:'.$font_size.'px; height:'.$font_size.'px; line-height:'.$font_size.'px;"';
		}
		$html .= '>'.$digit.'</span>';

    return $html;
}
}
add_shortcode('counter', 'counter');