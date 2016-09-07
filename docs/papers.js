$(document).ready(function () {
    main();
});

function main() {

    $('#papers').DataTable({
        ajax: "data/gammacat-papers.json",
        columns: [
            {data: "id"},
            {data: "path"},
        ]
    });

}