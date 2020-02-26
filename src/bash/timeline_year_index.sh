#!/bin/bash
# arguments:
# $1: month of IPhO to be created
# $2: previous month if exists, 0 otherwise
# $3: next month if exists, 0 otherwise
echo "Creating timeline/$1/index"
# imports
source countrycodes.sh
source ordinals.sh
source header_side.sh 1
source footer.sh
# load file and replace basics
html="$(cat templates/timeline/month/index.html)"
html="${html//__HEADER_SIDE__/$header_side}"
html="${html//__FOOTER__/$footer}"

while IFS=, read number month date code city homepage p_country p_student gold silver bronze honourable newline
do
    if [ $1 == $month ]
    then
        html="${html//__NUMBER__/$number}"
        html="${html//__ORDINAL__/${ordinals[$number]}}"
        html="${html//__MONTH__/$month}"
        html="${html//__DATE__/$date}"
        html="${html//__CODE__/$code}"
        html="${html//__COUNTRY__/${countrycodes[$code]}}"
        if [ "$city" != "" ]
        then
            html="${html//__CITY__/$city, }"
        else
            html="${html//__CITY__/}"
        fi
        if [ $2 != 0 ]
        then
            previous_month_html="$(cat templates/timeline/month/index_previous_month.html)"
            previous_month_html="${previous_month_html//__PREVIOUS_MONTH__/$2}"
            html="${html//__PREVIOUS_MONTH__/$previous_month_html}"
        else
            html="${html//__PREVIOUS_MONTH__/}"
        fi
        if [ $3 != 0 ]
        then
            next_month_html="$(cat templates/timeline/month/index_next_month.html)"
            next_month_html="${next_month_html//__NEXT_MONTH__/$3}"
            html="${html//__NEXT_MONTH__/$next_month_html}"
        else
            html="${html//__NEXT_MONTH__/}"
        fi
        if [ "$p_country" != "" ]
        then
            p_country_html="$(cat templates/timeline/month/index_p_country.html)"
            p_country_html="${p_country_html//__P_COUNTRY__/$p_country}"
            html="${html//__P_COUNTRY__/$p_country_html}"
        else
            html="${html//__P_COUNTRY__/}"
        fi
        if [ "$p_student" != "" ]
        then
            p_student_html="$(cat templates/timeline/month/index_p_student.html)"
            p_student_html="${p_student_html//__P_STUDENT__/$p_student}"
            html="${html//__P_STUDENT__/$p_student_html}"
        else
            html="${html//__P_STUDENT__/}"
        fi
        if [ "$homepage" != "" ]
        then
            homepage_html="$(cat templates/timeline/month/index_homepage.html)"
            homepage_html="${homepage_html//__HOMEPAGE__/$homepage}"
            homepage_html="${homepage_html//__MONTH__/$month}"
            html="${html//__HOMEPAGE__/$homepage_html}"
        else
            html="${html//__HOMEPAGE__/}"
        fi
        if [ "$gold" != "" ]
        then
            awards_html="$(cat templates/timeline/month/index_awards.html)"
            awards_html="${awards_html//__GOLD__/$gold}"
            awards_html="${awards_html//__SILVER__/$silver}"
            awards_html="${awards_html//__BRONZE__/$bronze}"
            awards_html="${awards_html//__HONOURABLE__/$honourable}"
            html="${html//__AWARDS__/$awards_html}"
        else
            html="${html//__AWARDS__/}"
        fi
    fi
done < database/timeline.csv
# final replacements and export
html="${html//__BASE__/../..}"
source final_replacer.sh
echo "$html" > ../timeline/$1/index.html