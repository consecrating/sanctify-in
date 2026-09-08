<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<?php 
global $qode_options_sanctify;
global $wp_query;
$disable_qode_seo = "";
$seo_title = "";
if (isset($qode_options_sanctify['disable_qode_seo'])) $disable_qode_seo = $qode_options_sanctify['disable_qode_seo'];
if ($disable_qode_seo != "yes") {
	$seo_title = get_post_meta($wp_query->get_queried_object_id(), "qode_seo_title", true);
	$seo_description = get_post_meta($wp_query->get_queried_object_id(), "qode_seo_description", true);
	$seo_keywords = get_post_meta($wp_query->get_queried_object_id(), "qode_seo_keywords", true);
}
?>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	<?php
	$responsiveness = "yes";
	if (isset($qode_options_sanctify['responsiveness'])) $responsiveness = $qode_options_sanctify['responsiveness'];
	if($responsiveness != "no"):
	?>
	<meta name=viewport content="width=device-width,initial-scale=1">
	<?php 
	endif;
	?>
	<?php
// Let WordPress + SEO plugin handle the title
if ( ! current_theme_supports( 'title-tag' ) ) {
    add_theme_support( 'title-tag' );
}
?>
<?php if ($disable_qode_seo != "yes") { ?>
	<?php if($seo_description) { ?>
	<meta name="description" content="<?php echo $seo_description; ?>">
	<?php } else if($qode_options_sanctify['meta_description']){ ?>
	<meta name="description" content="<?php echo $qode_options_sanctify['meta_description'] ?>">
	<?php } ?>
	<?php if($seo_keywords) { ?>
	<meta name="keywords" content="<?php echo $seo_keywords; ?>">
	<?php } else if($qode_options_sanctify['meta_keywords']){ ?>
	<meta name="keywords" content="<?php echo $qode_options_sanctify['meta_keywords'] ?>">
	<?php } ?>
	<?php } ?>
	<link rel="profile" href="http://gmpg.org/xfn/11" />
	<link rel="pingback" href="<?php bloginfo( 'pingback_url' ); ?>" />
	<link rel="shortcut icon" type="image/x-icon" href="<?php echo $qode_options_sanctify['favicon_image']; ?>">
	<?php wp_head(); ?>
	
</head>

<body <?php body_class(); ?>>
	
	<!-- Google Analytics start -->
	<?php if (isset($qode_options_sanctify['google_analytics_code'])){
				if($qode_options_sanctify['google_analytics_code'] != "") { 
	?>
		<script>
			var _gaq = _gaq || [];
			_gaq.push(['_setAccount', '<?php echo $qode_options_sanctify['google_analytics_code']; ?>']);
			_gaq.push(['_trackPageview']);

			(function() {
				var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
				ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
				var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
			})();
		</script>
	<?php }
		}
	?>
	<!-- Google Analytics end -->
	
<div class="wrapper">
<?php
	$header_fixed = false;
	if ($qode_options_sanctify['header_fixed'] == "yes") $header_fixed = true;
	
	$centered_logo = false;
	if ($qode_options_sanctify['center_logo_image'] == "yes") $centered_logo = true;
?>
<header class="<?php if($header_fixed){ echo 'header_top_fixed'; } ?> <?php if($centered_logo){ echo ' centered_logo'; } ?>">
	
	<?php	
	$display_header_widget = $qode_options_sanctify['header_widget_area'];
	if (!empty($_SESSION['qode_top_menu']))
		$display_header_widget = $_SESSION['qode_top_menu'];
	if($display_header_widget == "yes"){ ?> 
	<div class="header_top_outer">
		<div class="header_top_middle">
			<div class="header_top_inner">
				<div class="header_top_left">
					<?php dynamic_sidebar('header_left'); ?>
				</div>
				<div class="header_top_right">
					<?php dynamic_sidebar('header_right'); ?>
				</div>
			</div>
		</div>
	</div>
	<?php } ?>
	<div class="header_inner">
		<div class="container">
			<div class="container_inner clearfix">
				<div class="logo"><a href="<?php echo home_url(); ?>/"><img src="<?php echo $qode_options_sanctify['logo_image']; ?>" alt="Logo"/></a></div>
				<?php
				$menu_type = $qode_options_sanctify['top_menu'];
				if (!empty($_SESSION['qode_menu']))
					$menu_type = $_SESSION['qode_menu'];
					
				$fisrt_level_type = $qode_options_sanctify['first_level_type'];
				if (!empty($_SESSION['qode_first_level_type']))
					$fisrt_level_type = $_SESSION['qode_first_level_type'];
					
				$separator_type = $qode_options_sanctify['first_level_separator_type'];
				if (!empty($_SESSION['qode_first_level_separator_type']))
					$separator_type = $_SESSION['qode_first_level_separator_type'];
				?>
				<nav class="main_nav <?php if($fisrt_level_type == "normal") { echo "main_menu2"; }else{ echo "main_menu"; } ?> <?php if($separator_type == "elegant") { echo "separator_elegant"; }else{ echo "separator_regular"; } ?> <?php if($menu_type == "drop_down1") { echo "drop_down"; } elseif($menu_type == "drop_down2") { echo "drop_down2"; } else { echo "drop_down3"; } ?>">
				<?php
					
					if($menu_type == "drop_down1"):
						wp_nav_menu( array( 'theme_location' => 'top-navigation' , 
																'container'  => '', 
																'container_class' => '', 
																'menu_class' => '', 
																'menu_id' => '',
																'fallback_cb' => 'top_navigation_fallback',
																'walker' => new qode_type1_walker_nav_menu()
						 ));
						 
					elseif($menu_type == "drop_down2") :
						wp_nav_menu( array( 'theme_location' => 'top-navigation' , 
																'container'  => '', 
																'container_class' => '', 
																'menu_class' => '', 
																'menu_id' => '',
																'fallback_cb' => 'top_navigation_fallback',
																'walker' => new qode_type2_walker_nav_menu()
					 ));
					
					else :
						wp_nav_menu( array( 'theme_location' => 'top-navigation' , 
																'container'  => '', 
																'container_class' => '', 
																'menu_class' => '', 
																'menu_id' => '',
																'fallback_cb' => 'top_navigation_fallback',
																'walker' => new qode_type3_walker_nav_menu()
						 ));
					endif;
				?>
				
				</nav>
				<nav class="selectnav"></nav>
			</div>
		</div>
	</div>
	<div class="separator_holder"></div>
</header>
	<div class="content">
		<?php 
global $wp_query;
$id = $wp_query->get_queried_object_id();
$animation = get_post_meta($id, "qode_show-animation", true);
if (!empty($_SESSION['qode_animation']) && $animation == "")
	$animation = $_SESSION['qode_animation'];
?>
			<?php if($qode_options_sanctify['page_transitions'] == "1" || $qode_options_sanctify['page_transitions'] == "2" || $qode_options_sanctify['page_transitions'] == "3" || $qode_options_sanctify['page_transitions'] == "4" || ($animation == "updown") || ($animation == "fade") || ($animation == "updown_fade") || ($animation == "leftright")){ ?>
				<div class="meta">				
					<?php if($seo_title){ ?>
						<div class="seo_title"><?php bloginfo('name'); ?> | <?php echo $seo_title; ?></div>
					<?php } else{ ?>
						<div class="seo_title"><?php bloginfo('name'); ?> | <?php is_front_page() ? bloginfo('description') : wp_title(''); ?></div>
					<?php } ?>
					<?php if($seo_description){ ?>
						<div class="seo_description"><?php echo $seo_description; ?></div>
					<?php } else if($qode_options_sanctify['meta_description']){?>
						<div class="seo_description"><?php echo $qode_options_sanctify['meta_description']; ?></div>
					<?php } ?>
					<?php if($seo_keywords){ ?>
						<div class="seo_keywords"><?php echo $seo_keywords; ?></div>
					<?php }else if($qode_options_sanctify['meta_keywords']){?>
						<div class="seo_keywords"><?php echo $qode_options_sanctify['meta_keywords']; ?></div>
					<?php }?>
					<span id="qode_page_id"><?php echo $wp_query->get_queried_object_id(); ?></span>
					<div class="body_classes"><?php echo implode( ',', get_body_class()); ?></div>
				</div>
			<?php } ?>
			<div class="content_inner <?php echo $animation;?> ">
				
</script>
<script>

</script>