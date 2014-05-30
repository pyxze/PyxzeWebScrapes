<?php

foreach (range(1,449) as $i) {

    $html = file_get_contents('http://trancearoundtheworld.com/tatw/' . $i);
    $doc = new DOMDocument();
    libxml_use_internal_errors(TRUE);
    $doc->loadHTML($html);
    libxml_clear_errors();
    $xpath = new DOMXpath($doc);
    $el = $xpath->query('//*[@id="extension"]');
    file_put_contents(str_pad($i, 3, '0', STR_PAD_LEFT) . ".txt", $el->item(0)->textContent);

}
