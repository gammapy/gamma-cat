// Utility functions


// http://stackoverflow.com/a/2998822/498873
function zero_pad_string(num, size) {
    var s = "000000000" + num;
    return s.substr(s.length - size);
}

function render_tgevcat(data, type, row, meta) {
    return row.tgevcat_name + ' ' + row.tgevcat_id;
}

function render_tevcat(data, type, row, meta) {
    return row.tevcat_name + ' ' + render_tevcat_url(row.tevcat_id) + ' ' + render_tevcat2_url(row.tevcat2_id);
}

function render_tevcat_url(val) {
    return "<a href=\"http://tevcat.uchicago.edu/?mode=1&showsrc=" + val + "\">" + val + "</a>";
}

function render_tevcat2_url(val) {
    return "<a href=\"http://tevcat2.uchicago.edu/sources/" + val + "\">" + val + "</a>";
}

function render_ads_url(reference_id) {
    var dataset_url = reference_id;
    return "<a href=\"https://ui.adsabs.harvard.edu/#abs/" + dataset_url + "\">" + reference_id + "</a>";
}

function render_dataset_github_url(val) {
    return "<a href=\"https://github.com/gammapy/gamma-cat/tree/master/input/data/" + val + "\">" + val + "</a>";
}

function render_source_github_url(source_id) {
    var text = zero_pad_string(source_id, 6)
    var filename = "tev-" + text + ".yaml";
    return "<a href=\"https://github.com/gammapy/gamma-cat/blob/master/input/sources/" + filename + "\">" + text + "</a>";
}