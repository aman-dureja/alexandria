#!/usr/bin/env bash

# MAKE SURE YOU HAVE EXECUTE PERMISSIONS
#
BOOK_TITLE=${1}
SNIPPET=${2}
NUM=${3}
# RESOLVED_BOOK_TITLE=${2}
# SNIPPETS=${2}
#

URL="https://alexandria-c0235.firebaseio.com/books/"
RESOLVED_URL_1=$URL$RESOLVED_BOOK_TITLE
echo $RESOLVED_URL_1
FILE_TYPE=".json"

RESOLVED_URL_2="${RESOLVED_URL_1}.json"
RESOLVED_URL_2+=".json"
echo $RESOLVED_URL_2

curl -X PUT -d '{ "1": "Produced by Michael Lockey and PG Distributed Proofreaders[Illustration: He smashed down upon me again, and made that hole in myleg above the knee. I handled my knife in a hurry, and made more thanone hole in his skin, while he stuck a prong through my arm.]WILD NORTHERN SCENES.SPORTING ADVENTURESTHE RIFLE AND THE ROD.BY S. H. HAMMOND.TO JOHN H. REYNOLDS, ESQ., OF ALBANY. You have floated over the beautiful lakes and along the pleasant", "2": "rivers of that broad wilderness lying between the majestic St.Lawrence and Lake Champlain. You have, in seasons of relaxation fromthe labors of a profession in which you have achieved such enviable distinction, indulged in the sports pertaining to that wild region.You have listened to the gladmusic of the woods when the morning wasyoung, and to the solemn night voices of the forest when darknessenshrouded the earth. You are, therefore, familiar with the scenerydescribed in the following pages.Permit me, then, to dedicate this book to you, not because of youreminence as a lawyer, nor yet on account of your distinguished", "3": "position as a citizen, but as a keen, intelligent sportsman, one wholoves nature in her primeval wildness, and who is at home, with arifle and rod, in the old woods.With sentiments of great respect,I remain your friend and servant,THE AUTHOR.There is a broad sweep of country lying between the St. Lawrence andLake Champlain, which civilization with its improvements and its rushof progress has not yet invaded. It is mountainous, rocky, and for allagricultural purposes sterile and unproductive. It is covered with", "4": "dense forests, and inhabited by the same wild things, save the red manalone, that were there thousands of years ago. It abounds in the most beautiful lakes that the sun or the stars ever shone upon. I havestood upon the immense boulder that forms the head or summit of Baldface Mountain, a lofty, isolated peak, looming thousands of feettowards the sky, and counted upwards of twenty of these beautifullakes--sleeping in quiet beauty in their forest beds, surroundedby primeval woods, overlooked by rugged hills, and their placid watersglowing in the sunlight.It is a high region, from which numerous rivers take their rise to" }' 'https://alexandria-c0235.firebaseio.com/books/WildNorthernScene/snippets.json'
