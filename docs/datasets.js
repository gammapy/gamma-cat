$(document).ready(function () {
    main();
});

function main() {

    $('#datasets').DataTable({
        ajax: "data/gammacat-datasets.json",
        columns: [
            {
                data: "id",
                render: render_ads_url
            },
            {
                data: "url",
                render: render_dataset_github_url
            },
        ]
    });

}
