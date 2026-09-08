<?php
/**
 * Prove the split_html_tags() fix in isolation, with no WordPress present.
 *
 * Asserts three things:
 *   1. The reconstruction invariant holds - concatenating every part reproduces
 *      the input byte for byte. If this breaks, the plugin would corrupt pages.
 *   2. JSON-LD inside <script type="application/ld+json"> is marked protected,
 *      so no keyword link can be injected and the JSON stays valid.
 *   3. Ordinary body text is still marked replaceable, so the plugin keeps
 *      working as intended.
 */

// Extract the two functions from both versions and run them side by side.
function load_class(string $file, string $classname): string {
    $src = file_get_contents($file);
    $src = preg_replace('/^<\?php/', '', $src, 1);
    $src = str_replace("if (!defined('ABSPATH')) exit;", '', $src);
    // Rename every reference, including the bootstrap call at the end of file.
    $src = str_replace('AutoKeywordLinks', $classname, $src);
    return $src;
}

// Minimal WP stubs so the class body parses and instantiates.
if (!function_exists('register_activation_hook'))   { function register_activation_hook() {} }
if (!function_exists('register_deactivation_hook')) { function register_deactivation_hook() {} }
if (!function_exists('register_uninstall_hook'))    { function register_uninstall_hook() {} }
if (!function_exists('plugin_basename'))            { function plugin_basename($f) { return $f; } }
if (!function_exists('plugin_dir_url'))             { function plugin_dir_url($f) { return ''; } }
if (!function_exists('plugin_dir_path'))            { function plugin_dir_path($f) { return ''; } }
if (!function_exists('wp_enqueue_script'))          { function wp_enqueue_script() {} }
if (!function_exists('wp_enqueue_style'))           { function wp_enqueue_style() {} }
if (!function_exists('add_action'))     { function add_action() {} }
if (!function_exists('add_filter'))     { function add_filter() {} }
if (!function_exists('esc_url'))        { function esc_url($u) { return $u; } }
if (!function_exists('esc_html'))       { function esc_html($t) { return $t; } }
if (!function_exists('esc_attr'))       { function esc_attr($t) { return $t; } }
if (!function_exists('get_option'))     { function get_option($k, $d = false) { return $d; } }
if (!function_exists('update_option'))  { function update_option() { return true; } }
if (!function_exists('__'))             { function __($t, $d = null) { return $t; } }
if (!function_exists('esc_html__'))     { function esc_html__($t, $d = null) { return $t; } }
if (!function_exists('wp_kses_post'))   { function wp_kses_post($t) { return $t; } }
if (!function_exists('sanitize_text_field')) { function sanitize_text_field($t) { return $t; } }
if (!function_exists('current_user_can')) { function current_user_can() { return false; } }
if (!function_exists('is_admin'))       { function is_admin() { return false; } }
if (!function_exists('wp_unslash'))     { function wp_unslash($t) { return $t; } }
if (!function_exists('admin_url'))      { function admin_url($p = '') { return $p; } }
if (!function_exists('wp_nonce_field')) { function wp_nonce_field() {} }
if (!function_exists('check_admin_referer')) { function check_admin_referer() { return true; } }
if (!function_exists('wp_verify_nonce')) { function wp_verify_nonce() { return true; } }
if (!function_exists('wp_redirect'))    { function wp_redirect() {} }
if (!function_exists('add_menu_page'))  { function add_menu_page() {} }
if (!function_exists('add_submenu_page')) { function add_submenu_page() {} }
if (!defined('ABSPATH')) { define('ABSPATH', '/tmp/'); }

eval(load_class(__DIR__ . '/akl.php',       'AklOld'));
eval(load_class(__DIR__ . '/akl-fixed.php', 'AklNew'));

function parts_of(object $obj, string $html): array {
    $ref = new ReflectionMethod($obj, 'split_html_tags');
    $ref->setAccessible(true);
    return $ref->invoke($obj, $html);
}

$old = AklOld::instance();
$new = AklNew::instance();

// The real-world shape: valid JSON-LD whose description contains the keyword
// that the plugin auto-links.
$jsonld = '{"@context": "https://schema.org", "@graph": [{"@type": "Organization",'
        . ' "@id": "https://www.sanctify.in/#org", "name": "Sanctify",'
        . ' "description": "Award-winning advertising and digital marketing agency in Goa.",'
        . ' "areaServed": {"@type": "State", "name": "Goa, India"}}]}';

$html = "<p>We are a digital marketing agency in Goa serving clients.</p>\n"
      . '<script type="application/ld+json">' . $jsonld . "</script>\n"
      . "<p>Another digital marketing agency in Goa mention.</p>";

$pass = 0; $fail = 0;
function check(string $label, bool $ok, string $detail = ''): void {
    global $pass, $fail;
    if ($ok) { $pass++; echo "  PASS  $label\n"; }
    else     { $fail++; echo "  FAIL  $label\n"; if ($detail !== '') echo "        $detail\n"; }
}

echo "\n=== reconstruction invariant (must hold, else pages get corrupted) ===\n";
foreach (['OLD' => $old, 'NEW' => $new] as $name => $obj) {
    $parts = parts_of($obj, $html);
    $rebuilt = '';
    foreach ($parts as $p) { $rebuilt .= $p['content']; }
    check("$name rebuilds input byte-for-byte", $rebuilt === $html,
          'length ' . strlen($rebuilt) . ' vs ' . strlen($html));
}

echo "\n=== is the JSON-LD body protected from keyword replacement? ===\n";
foreach (['OLD' => $old, 'NEW' => $new] as $name => $obj) {
    $parts = parts_of($obj, $html);
    $exposed = false;
    foreach ($parts as $p) {
        if (!$p['tag'] && strpos($p['content'], '"@context"') !== false) { $exposed = true; }
        if (!$p['tag'] && strpos($p['content'], 'Award-winning advertising') !== false) { $exposed = true; }
    }
    if ($name === 'OLD') {
        check('OLD leaves JSON-LD EXPOSED (reproduces the reported bug)', $exposed,
              'expected the original to be buggy');
    } else {
        check('NEW protects JSON-LD', !$exposed,
              $exposed ? 'JSON-LD body is still replaceable' : '');
    }
}

echo "\n=== end-to-end: simulate the replacement and re-parse the JSON ===\n";
foreach (['OLD' => $old, 'NEW' => $new] as $name => $obj) {
    $parts = parts_of($obj, $html);
    $out = '';
    foreach ($parts as $p) {
        $text = $p['content'];
        if (!$p['tag']) {
            // exactly what the plugin does: wrap the keyword in an anchor
            $text = preg_replace(
                '/digital marketing agency in Goa/i',
                '<a href="https://www.sanctify.in/sanctify-facility/digital-marketing-agency-goa/"'
                . ' target="_blank" rel="noopener">Digital Marketing Agency in Goa</a>',
                $text
            );
        }
        $out .= $text;
    }
    preg_match('/<script[^>]*application\/ld\+json[^>]*>(.*?)<\/script>/is', $out, $m);
    $decoded = json_decode($m[1] ?? '', true);
    $valid = json_last_error() === JSON_ERROR_NONE && is_array($decoded);
    if ($name === 'OLD') {
        check('OLD produces INVALID JSON (confirms root cause)', !$valid,
              'expected invalid, got ' . json_last_error_msg());
    } else {
        check('NEW produces VALID JSON', $valid, 'json_last_error: ' . json_last_error_msg());
        $linked = substr_count($out, '<a href="https://www.sanctify.in/sanctify-facility/');
        check('NEW still auto-links the body text (2 paragraphs)', $linked === 2,
              "found $linked links, expected 2");
        check('NEW leaves the schema description untouched',
              strpos($m[1] ?? '', 'Award-winning advertising and digital marketing agency in Goa.') !== false);
    }
}

echo "\n=== nested / edge cases ===\n";
$edges = [
    'empty string'                  => '',
    'text only'                     => 'digital marketing agency in Goa',
    'unclosed script'               => '<p>hi</p><script>var x = 1;',
    'two scripts'                   => '<script>a</script>mid<script>b</script>',
    'style block'                   => '<style>.a{color:red}</style>text',
    'existing anchor'               => '<a href="/x">digital marketing agency in Goa</a>',
    'pre block'                     => '<pre>digital marketing agency in Goa</pre>',
    'attribute containing gt'       => '<p title="a > b">digital marketing agency in Goa</p>',
];
foreach ($edges as $label => $sample) {
    $parts = parts_of($new, $sample);
    $rebuilt = '';
    foreach ($parts as $p) { $rebuilt .= $p['content']; }
    check("NEW rebuilds: $label", $rebuilt === $sample,
          'got ' . var_export($rebuilt, true));
}

echo "\n";
echo "passed $pass, failed $fail\n";
exit($fail === 0 ? 0 : 1);
