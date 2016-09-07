// TODO: use row detail for papers.
// See https://datatables.net/examples/api/row_details.html

// http://stackoverflow.com/a/2998822/498873
function pad(num, size) {
    var s = "000000000" + num;
    return s.substr(s.length - size);
}

$(document).ready(function () {
    main();
});

function main() {

    $('#sources').DataTable({
        ajax: "data/gammacat-sources.json",
        columns: [
            {
                data: "source_id",
                render: function (val) {
                    var source_id = pad(val, 6)
                    var filename = "tev-" + source_id + ".yaml";
                    return "<a href=\"https://github.com/gammapy/gamma-cat/blob/master/input/sources/" + filename + "\">" + source_id + "</a>";
                }
            },
            {data: "common_name"},
            {
                data: "tevcat_id",
                render: function (val) {
                    return "<a href=\"http://tevcat.uchicago.edu/?mode=1&showsrc=" + val + "\">" + val + "</a>";
                }
            },
            {
                data: "tevcat2_id",
                render: function (val) {
                    return "<a href=\"http://tevcat2.uchicago.edu/sources/" + val + "\">" + val + "</a>";
                }
            },
            {data: "tevcat_name"},
            {data: "tgevcat_id"},
            {data: "tgevcat_name"},
            {
                data: "papers",
                render: function (val) {
                    return val.substr(0, 20);
                }
            }
        ]
    });

}