FROM docker.elastic.co/elasticsearch/elasticsearch:7.10.0 AS elastic-raudikko

RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install https://github.com/EvidentSolutions/elasticsearch-analysis-raudikko/releases/download/v0.1/elasticsearch-analysis-raudikko-0.1-es7.10.0.zip