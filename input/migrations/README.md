# Input data schema migrations

A [schema migration](https://en.wikipedia.org/wiki/Schema_migration)
is a change in format.
An example would be renaming a field from `RAJ2000` to `ra`.

While we are adding data to `gamma-cat`, and as our experience and use
cases evolve, we will have to change our formats from time to time.

Sometimes it's possible to edit files by hand, or to use an IDE or
command like tool like [sed](https://en.wikipedia.org/wiki/Sed) to make
a change to many files. Sometimes one can write a Python script to do
the migration.

In any case, please check the diff locally or on Github when touching
many files, to make sure the changes are good.

You can use this folder to put Python scripts or notes that you've used
for schema migrations.
