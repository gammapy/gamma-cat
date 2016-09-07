$(document).ready(function () {
    main();
});

function main() {

    $('#papers').DataTable({
        ajax: "data/gammacat-papers.json",
        columns: [
            {
                data: "id",
                render: function (val) {
                    var url_val = val;
                    return "<a href=\"https://ui.adsabs.harvard.edu/#abs/" + url_val + "\">" + val + "</a>";
                }
            },
            {
                data: "url",
                render: function (val) {
                    return "<a href=\"https://github.com/gammapy/gamma-cat/tree/master/input/papers/" + val + "\">" + val + "</a>";
                }
            },
        ]
    });

}
