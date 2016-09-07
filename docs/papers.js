$(document).ready(function () {
    main();
});

function main() {

    $('#papers').DataTable({
        ajax: "data/gammacat-papers.json",
        columns: [
            {
                data: "id",
                render: render_ads_url
            },
            {
                data: "url",
                render: render_paper_github_url
            },
        ]
    });

}
