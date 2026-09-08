<?php
/**
 * Plugin Name: Auto Keyword Links
 * Description: Automatically interlink keywords to URLs in your content with priority, variations, and settings.
 * Version: 1.0
 * Author: Your Name
 */

if (!defined('ABSPATH')) exit;

class AutoKeywordLinks {
    private static $instance = null;
    private $option_key = 'akl_rules';
    private $defaults = array(
        'rules' => array(),
        'settings' => array(
            'limit_per_page' => 5,
            'open_in_new_tab' => true,
            'nofollow' => false,
            'case_sensitive' => false,
            'whole_word' => true,
            'replace_first_only' => true,
            'exclude_post_types' => array('attachment'),
        ),
    );

    public static function instance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        register_activation_hook(__FILE__, array($this, 'activate'));
        add_action('admin_menu', array($this, 'admin_menu'));
        add_action('admin_init', array($this, 'handle_post'));
        add_filter('the_content', array($this, 'filter_content'), 999);
    }

    public function activate() {
        if (get_option($this->option_key) === false) {
            update_option($this->option_key, $this->defaults);
        }
    }

    private function get_options() {
        $opts = get_option($this->option_key, $this->defaults);
        return wp_parse_args($opts, $this->defaults);
    }

    private function update_options($opts) {
        update_option($this->option_key, $opts);
    }

    public function admin_menu() {
        add_menu_page('Auto Keyword Links', 'Auto Keyword Links', 'manage_options', 'akl_rules', array($this, 'admin_rules_page'), 'dashicons-admin-links', 60);
        add_submenu_page('akl_rules', 'Settings', 'Settings', 'manage_options', 'akl_settings', array($this, 'admin_settings_page'));
    }

    public function handle_post() {
        if (!current_user_can('manage_options')) return;

        if (isset($_POST['akl_action']) && check_admin_referer('akl_save', 'akl_nonce')) {
            $opts = $this->get_options();

            if ($_POST['akl_action'] === 'save_rule') {
                $rules = $opts['rules'];
                $rule = array(
                    'keyword' => sanitize_text_field($_POST['keyword']),
                    'url' => esc_url_raw($_POST['url']),
                    'variations' => array_filter(array_map('trim', explode("\n", sanitize_textarea_field($_POST['variations'])))),
                    'priority' => intval($_POST['priority']),
                    'enabled' => isset($_POST['enabled']) ? 1 : 0,
                );
                $index = isset($_POST['rule_index']) ? intval($_POST['rule_index']) : null;
                if ($index !== null && isset($rules[$index])) {
                    $rules[$index] = $rule;
                } else {
                    $rules[] = $rule;
                }
                // Sort by priority desc
                usort($rules, function($a, $b) { return $b['priority'] - $a['priority']; });
                $opts['rules'] = $rules;
                $this->update_options($opts);
                wp_redirect(admin_url('admin.php?page=akl_rules&saved=1'));
                exit;
            }

            if ($_POST['akl_action'] === 'save_settings') {
                $s = $opts['settings'];
                $s['limit_per_page'] = max(1, intval($_POST['limit_per_page']));
                $s['open_in_new_tab'] = isset($_POST['open_in_new_tab']);
                $s['nofollow'] = isset($_POST['nofollow']);
                $s['case_sensitive'] = isset($_POST['case_sensitive']);
                $s['whole_word'] = isset($_POST['whole_word']);
                $s['replace_first_only'] = isset($_POST['replace_first_only']);
                $s['exclude_post_types'] = isset($_POST['exclude_post_types']) ? array_map('sanitize_text_field', $_POST['exclude_post_types']) : array();
                $opts['settings'] = $s;
                $this->update_options($opts);
                wp_redirect(admin_url('admin.php?page=akl_settings&saved=1'));
                exit;
            }
        }

        // Delete rule
        if (isset($_GET['akl_action'], $_GET['rule']) && $_GET['akl_action'] === 'delete' && check_admin_referer('akl_delete_' . intval($_GET['rule']))) {
            $opts = $this->get_options();
            $rules = $opts['rules'];
            $index = intval($_GET['rule']);
            if (isset($rules[$index])) {
                unset($rules[$index]);
                $opts['rules'] = array_values($rules);
                $this->update_options($opts);
            }
            wp_redirect(admin_url('admin.php?page=akl_rules&deleted=1'));
            exit;
        }
    }

    public function admin_rules_page() {
        if (!current_user_can('manage_options')) wp_die('Unauthorized');
        $opts = $this->get_options();
        $rules = $opts['rules'];
        $edit_index = isset($_GET['edit']) ? intval($_GET['edit']) : null;
        $edit_rule = $edit_index !== null && isset($rules[$edit_index]) ? $rules[$edit_index] : null;
        ?>
        <div class="wrap">
            <h1>Auto Keyword Links - Rules</h1>
            <?php if (isset($_GET['saved'])) echo '<div class="updated notice"><p>Rule saved.</p></div>'; ?>
            <?php if (isset($_GET['deleted'])) echo '<div class="updated notice"><p>Rule deleted.</p></div>'; ?>
            <table class="widefat fixed" cellspacing="0">
                <thead><tr><th>Keyword</th><th>URL</th><th>Priority</th><th>Enabled</th><th>Actions</th></tr></thead>
                <tbody>
                <?php foreach ($rules as $i => $r): ?>
                    <tr>
                        <td><?php echo esc_html($r['keyword']); ?></td>
                        <td><a href="<?php echo esc_url($r['url']); ?>" target="_blank" rel="noopener"><?php echo esc_html($r['url']); ?></a></td>
                        <td><?php echo intval($r['priority']); ?></td>
                        <td><?php echo $r['enabled'] ? 'Yes' : 'No'; ?></td>
                        <td>
                            <a href="<?php echo admin_url('admin.php?page=akl_rules&edit=' . $i); ?>">Edit</a> |
                            <?php wp_nonce_field('akl_delete_' . $i); ?>
                            <a href="<?php echo wp_nonce_url(admin_url('admin.php?page=akl_rules&akl_action=delete&rule=' . $i), 'akl_delete_' . $i); ?>" onclick="return confirm('Delete this rule?');">Delete</a>
                        </td>
                    </tr>
                <?php endforeach; ?>
                </tbody>
            </table>

            <h2><?php echo $edit_rule ? 'Edit Rule' : 'Add New Rule'; ?></h2>
            <form method="post">
                <?php wp_nonce_field('akl_save', 'akl_nonce'); ?>
                <input type="hidden" name="akl_action" value="save_rule">
                <input type="hidden" name="rule_index" value="<?php echo $edit_rule ? intval($edit_index) : ''; ?>">
                <table class="form-table">
                    <tr>
                        <th><label for="keyword">Keyword</label></th>
                        <td><input type="text" name="keyword" id="keyword" value="<?php echo $edit_rule ? esc_attr($edit_rule['keyword']) : ''; ?>" class="regular-text" required></td>
                    </tr>
                    <tr>
                        <th><label for="url">URL</label></th>
                        <td><input type="url" name="url" id="url" value="<?php echo $edit_rule ? esc_url($edit_rule['url']) : ''; ?>" class="regular-text" required></td>
                    </tr>
                    <tr>
                        <th><label for="variations">Variations (one per line)</label></th>
                        <td><textarea name="variations" id="variations" rows="4" class="large-text"><?php echo $edit_rule ? esc_textarea(implode("\n", $edit_rule['variations'])) : ''; ?></textarea></td>
                    </tr>
                    <tr>
                        <th><label for="priority">Priority</label></th>
                        <td><input type="number" name="priority" id="priority" value="<?php echo $edit_rule ? intval($edit_rule['priority']) : 10; ?>" class="small-text" required></td>
                    </tr>
                    <tr>
                        <th><label for="enabled">Enabled</label></th>
                        <td><input type="checkbox" name="enabled" id="enabled" <?php checked($edit_rule ? $edit_rule['enabled'] : 1, 1); ?>></td>
                    </tr>
                </table>
                <?php submit_button($edit_rule ? 'Update Rule' : 'Add Rule'); ?>
            </form>
        </div>
        <?php
    }

    public function admin_settings_page() {
        if (!current_user_can('manage_options')) wp_die('Unauthorized');
        $opts = $this->get_options();
        $s = $opts['settings'];
        $post_types = get_post_types(array('public' => true), 'objects');
        ?>
        <div class="wrap">
            <h1>Auto Keyword Links - Settings</h1>
            <?php if (isset($_GET['saved'])) echo '<div class="updated notice"><p>Settings saved.</p></div>'; ?>
            <form method="post">
                <?php wp_nonce_field('akl_save', 'akl_nonce'); ?>
                <input type="hidden" name="akl_action" value="save_settings">
                <table class="form-table">
                    <tr>
                        <th><label for="limit_per_page">Limit links per page</label></th>
                        <td><input type="number" name="limit_per_page" id="limit_per_page" value="<?php echo intval($s['limit_per_page']); ?>" class="small-text" min="1" required></td>
                    </tr>
                    <tr>
                        <th><label for="open_in_new_tab">Open links in new tab</label></th>
                        <td><input type="checkbox" name="open_in_new_tab" id="open_in_new_tab" <?php checked($s['open_in_new_tab'], true); ?>></td>
                    </tr>
                    <tr>
                        <th><label for="nofollow">Add nofollow attribute</label></th>
                        <td><input type="checkbox" name="nofollow" id="nofollow" <?php checked($s['nofollow'], true); ?>></td>
                    </tr>
                    <tr>
                        <th><label for="case_sensitive">Case sensitive matching</label></th>
                        <td><input type="checkbox" name="case_sensitive" id="case_sensitive" <?php checked($s['case_sensitive'], true); ?>></td>
                    </tr>
                    <tr>
                        <th><label for="whole_word">Match whole words only</label></th>
                        <td><input type="checkbox" name="whole_word" id="whole_word" <?php checked($s['whole_word'], true); ?>></td>
                    </tr>
                    <tr>
                        <th><label for="replace_first_only">Replace first occurrence only per keyword</label></th>
                        <td><input type="checkbox" name="replace_first_only" id="replace_first_only" <?php checked($s['replace_first_only'], true); ?>></td>
                    </tr>
                    <tr>
                        <th>Exclude post types</th>
                        <td>
                            <?php foreach ($post_types as $pt): ?>
                                <label><input type="checkbox" name="exclude_post_types[]" value="<?php echo esc_attr($pt->name); ?>" <?php echo in_array($pt->name, $s['exclude_post_types']) ? 'checked' : ''; ?>> <?php echo esc_html($pt->label); ?></label><br>
                            <?php endforeach; ?>
                        </td>
                    </tr>
                </table>
                <?php submit_button('Save Settings'); ?>
            </form>
        </div>
        <?php
    }

    public function filter_content($content) {
        if (is_admin()) return $content;

        global $post;
        if (!$post) return $content;

        $opts = $this->get_options();
        $settings = $opts['settings'];

        if (in_array(get_post_type($post), $settings['exclude_post_types'])) return $content;

        if (empty($opts['rules'])) return $content;

        $limit = max(1, intval($settings['limit_per_page']));
        $case_flag = $settings['case_sensitive'] ? '' : 'i';
        $whole_word = $settings['whole_word'];
        $replace_first_only = $settings['replace_first_only'];

        // Build patterns
        $patterns = array();
        foreach ($opts['rules'] as $idx => $rule) {
            if (empty($rule['enabled'])) continue;
            $keywords = array($rule['keyword']);
            if (!empty($rule['variations'])) {
                $keywords = array_merge($keywords, $rule['variations']);
            }
            foreach ($keywords as $kw) {
                $kw = trim($kw);
                if ($kw === '') continue;
                $escaped = preg_quote($kw, '/');
                if ($whole_word) {
                    $escaped = '(?<=^|\W)' . $escaped . '(?=$|\W)';
                }
                $patterns[] = array(
                    'pattern' => '/' . $escaped . '/' . $case_flag,
                    'keyword' => $kw,
                    'url' => $rule['url'],
                    'priority' => $rule['priority'],
                    'rule_index' => $idx,
                );
            }
        }

        // Sort by priority desc
        usort($patterns, function($a, $b) { return $b['priority'] - $a['priority']; });

        // Avoid replacing inside existing links, code, pre, script, style tags
        $parts = $this->split_html_tags($content);

        $total_links = 0;
        foreach ($parts as $i => $part) {
            if ($part['tag']) continue; // skip tags
            $text = $part['content'];
            if (trim($text) === '') continue;

            foreach ($patterns as $p) {
                if ($total_links >= $limit) break 2;
                $replacement = $this->build_anchor($p['keyword'], $p['url'], $settings);
                $count = $replace_first_only ? 1 : ($limit - $total_links);
                $new_text = preg_replace($p['pattern'], $replacement, $text, $count, $replaced_count);
                if ($replaced_count > 0) {
                    $text = $new_text;
                    $total_links += $replaced_count;
                }
            }
            $parts[$i]['content'] = $text;
        }

        // Rebuild content
        $out = '';
        foreach ($parts as $p) {
            $out .= $p['content'];
        }
        
        // Remove any style attributes from auto-generated links
        $out = preg_replace('/(<a\b[^>]*?)\s+(style|color|bgcolor|text-decoration|font-color|font-style|font-weight|text-transform)\s*=\s*["\'][^"\']*["\']/si', '$1', $out);
        
        return $out;
    }

    private function build_anchor($text, $url, $settings) {
        $target_attr = '';
        $rel = array();

        if ($settings['open_in_new_tab']) {
            $target_attr = ' target="_blank"';
            $rel[] = 'noopener';
        }
        if ($settings['nofollow']) {
            $rel[] = 'nofollow';
        }
        $rel_attr = '';
        if (!empty($rel)) {
            $rel_attr = ' rel="' . implode(' ', array_unique($rel)) . '"';
        }

        $anchor = '<a href="' . esc_url($url) . '"' . $target_attr . $rel_attr . '>' . esc_html($text) . '</a>';
        
        $anchor = preg_replace('/\s*(style|color|bgcolor|text-decoration|font-color|font-style|font-weight|text-transform|class)\s*=\s*["\'][^"\']*["\']/si', '', $anchor);
        
        return $anchor;
    }

    private function split_html_tags($html) {
        // Locate protected blocks FIRST, then split only what is left.
        //
        // The previous implementation split on every individual tag before
        // looking for <script>...</script>. That removed the wrapper, leaving the
        // body as ordinary text, so the later protection pattern could never
        // match. The visible symptom was keyword links injected inside
        // <script type="application/ld+json">, which made the JSON invalid and
        // produced structured-data errors on every affected page.
        //
        // preg_match_all with PREG_OFFSET_CAPTURE is used rather than preg_split:
        // this pattern has a nested capture group, and preg_split with
        // PREG_SPLIT_DELIM_CAPTURE emits every captured group, which would inject
        // bare tag names such as "script" straight into the content.
        $final = array();
        $protected = '/<(a|script|style|code|pre|textarea|noscript)\b[^>]*>.*?<\/\1\s*>/is';
        $offset = 0;

        if (preg_match_all($protected, $html, $matches, PREG_OFFSET_CAPTURE)) {
            foreach ($matches[0] as $hit) {
                $block_text = $hit[0];
                $block_pos  = $hit[1];
                if ($block_pos > $offset) {
                    $this->split_plain_segment(substr($html, $offset, $block_pos - $offset), $final);
                }
                $final[] = array('tag' => true, 'content' => $block_text);
                $offset = $block_pos + strlen($block_text);
            }
        }
        if ($offset < strlen($html)) {
            $this->split_plain_segment(substr($html, $offset), $final);
        }

        return $final;
    }

    /**
     * Split a segment that contains no protected blocks into tag and text parts.
     * Appends to $final by reference. Concatenating every part's content always
     * reproduces the input exactly.
     */
    private function split_plain_segment($segment, &$final) {
        if ($segment === '' || $segment === null) {
            return;
        }
        // Single capture group, so PREG_SPLIT_DELIM_CAPTURE is safe here.
        $pieces = preg_split('/(<[^>]+>)/', $segment, -1, PREG_SPLIT_DELIM_CAPTURE | PREG_SPLIT_NO_EMPTY);
        $buffer = '';
        foreach ($pieces as $piece) {
            if (strlen($piece) > 1 && $piece[0] === '<' && substr($piece, -1) === '>') {
                if ($buffer !== '') {
                    $final[] = array('tag' => false, 'content' => $buffer);
                    $buffer = '';
                }
                $final[] = array('tag' => true, 'content' => $piece);
            } else {
                $buffer .= $piece;
            }
        }
        if ($buffer !== '') {
            $final[] = array('tag' => false, 'content' => $buffer);
        }
    }
}

// Instantiate the plugin
AutoKeywordLinks::instance();
