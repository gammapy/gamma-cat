Overview about `{{ src_info.common_name }}`

Available Spectral energy distributions:

{% for sed in av_seds %}
* `{{ sed }} <../../../docs/data/data/{{sed.replace('&','%26')}}/gammacat_{{sed.replace('&','%26')}}_00000{{src_info.source_id}}_sed.ecsv>`__
{% endfor %}

