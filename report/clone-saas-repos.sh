#!/bin/bash

WORKDIR="$PWD/saas-repos"

rm -rf "$WORKDIR"; mkdir -p "$WORKDIR"

cd "$WORKDIR"

REPOS=`cat -`
echo "$REPOS" | xargs -P1 -n1 git clone -q

for saasrepo in `find "$WORKDIR" -mindepth 1 -maxdepth 1 -type d`; do
    cd "$saasrepo"

    project=`basename $saasrepo`
    repo=`echo "$REPOS" | grep "$project"`
    if grep -q "https://gitlab" <<< "$repo" && [[ ${#GITLAB_TOKEN} -gt 0 ]]; then
        TOKEN="--token $GITLAB_TOKEN"
    else
        TOKEN=""
    fi

    for context in $(saasherder config get-contexts); do
        for service in $(saasherder --environment production get-services --context $context); do
            hash_len=$(saasherder --context $context --environment production get hash $service | wc -c)
            [ "$hash_len" -eq "41" ] && saasherder --context $context --environment production update hash $service master
        done

        saasherder --context $context --environment production pull $TOKEN
        saasherder --context $context --environment production template --local tag
    done
done

