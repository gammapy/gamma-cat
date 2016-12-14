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
            {
                name: 'Common name',
                data: "common_name"
            },
            {
                name: "TGeVCat",
                render: render_tgevcat
            },
            {
                name: "TeVCat",
                render: render_tevcat
            },
            // TODO: use row detail for datasets
            // See https://datatables.net/examples/api/row_details.html
            {
                data: "datasets",
                render: function (val) {
                    return val.substr(0, 20);
                }
            }
        ]
    });

}