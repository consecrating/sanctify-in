<?php
/**
 * Plugin Name: Sanctify Term SEO (REST)
 * Description: Exposes SEOPress term-level SEO title and meta description over the REST API for category and post_tag, so archive SEO can be managed programmatically. Read/write requires manage_categories.
 * Version: 1.0
 * Author: Antigravity AI
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('init', function () {
    $taxonomies = array('category', 'post_tag');
    $keys = array(
        '_seopress_titles_title' => 'SEO title for this term archive',
        '_seopress_titles_desc'  => 'Meta description for this term archive',
    );

    foreach ($taxonomies as $taxonomy) {
        foreach ($keys as $key => $description) {
            register_term_meta($taxonomy, $key, array(
                'type'              => 'string',
                'single'            => true,
                'default'           => '',
                'description'       => $description,
                'show_in_rest'      => true,
                'sanitize_callback' => 'sanitize_text_field',
                // Term SEO is an editorial capability, so gate it on the same
                // capability WordPress uses for managing terms rather than
                // leaving it open to any authenticated user.
                'auth_callback'     => function () {
                    return current_user_can('manage_categories');
                },
            ));
        }
    }
}, 20);
