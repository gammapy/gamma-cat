$(document).ready(function () {
    main();
});

function main() {

    $('#sources').DataTable({
        ajax: "data/gammacat-sources.json",
        columns: [
            {
                data: "source_id",
                render: render_source_github_url
            },
            {data: "common_name"},
            {
                data: "tevcat_id",
                render: render_tevcat_url
            },
            {
                data: "tevcat2_id",
                render: render_tevcat2_url
            },
            {data: "tevcat_name"},
            {data: "tgevcat_id"},
            {data: "tgevcat_name"},

            // TODO: use row detail for papers.
            // See https://datatables.net/examples/api/row_details.html
            {
                data: "papers",
                render: function (val) {
                    return val.substr(0, 20);
                }
            }
        ]
    });

}