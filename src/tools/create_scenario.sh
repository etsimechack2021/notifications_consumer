#!/bin/bash

display_usage(){
	#Display Help
	echo 
	echo "This script creates the ETSI MEC Hackathon Scenario"
	echo
	echo "Usage: create_scenario.sh <parameter>"
	echo " - all: It creates drone UE and all subscriptions (location, rni, wai)"
	echo " - drone: It creates drone UE"
	echo " - location: It creates the location usertracking subscription"
	echo " - rni: It creates all the rni subscriptions"
	echo " - wai: It creates all the wai subscriptions"
	echo
}

create_drone_ue(){
	echo
	curl -X POST https://a-team.mec-hackathon-2021.interdigital.dev/sbxrh3d8f4/sandbox-ctrl/v1/events/SCENARIO-UPDATE \
	-H "accept: application/json" \
	-H "Content-Type: application/json" \
	-d "@drone_ue_creation.json"
	echo
	echo "Drone UE created"
}

create_location_subscriptions(){
	echo
	curl -X POST https://a-team.mec-hackathon-2021.interdigital.dev/sbxrh3d8f4/location/v2/subscriptions/userTracking \
	-H "accept: application/json" \
	-H "Content-Type: application/json" \
	-d "@location/drone_tracking_subscription.json"
	echo
	echo "UserTrackingSubscription created"
}

create_rni_subscriptions(){
	echo
	curl -X POST https://a-team.mec-hackathon-2021.interdigital.dev/sbxrh3d8f4/rni/v2/subscriptions \
	-H "accept: application/json" \
	-H "Content-Type: application/json" \
	-d "@rni/measrepue_subscription.json"
	echo
	echo "MeasRepUeSubscription created"
	
	curl -X POST https://a-team.mec-hackathon-2021.interdigital.dev/sbxrh3d8f4/rni/v2/subscriptions \
	-H "accept: application/json" \
	-H "Content-Type: application/json" \
	-d "@rni/nrmeasrepue_subscription.json"
	echo
	echo "NrMeasRepUeSubscription created"
}

create_wai_subscriptions(){
	echo
	curl -X POST https://a-team.mec-hackathon-2021.interdigital.dev/sbxrh3d8f4/wai/v2/subscriptions \
	-H "accept: application/json" \
	-H "Content-Type: application/json" \
	-d "@wai/assocsta_subscription_wifi.json"
	echo
	echo "Wifi AssocStaSubscription created"
	echo
	curl -X POST https://a-team.mec-hackathon-2021.interdigital.dev/sbxrh3d8f4/wai/v2/subscriptions \
	-H "accept: application/json" \
	-H "Content-Type: application/json" \
	-d "@wai/assocsta_subscription_nowifi.json"
	echo
	echo "No Wifi AssocStaSubscription created"	
}

if [ $# -eq 0 ]
	then
		display_usage
		exit 1
fi

if [ $1 = "drone" ];
	then
		create_drone_ue
		exit 0
fi

if [ $1 = "location" ];
	then
		create_location_subscriptions
		exit 0
fi

if [ $1 = "rni" ];
	then
		echo "Creating rni subscriptions..."
		create_rni_subscriptions
		exit 0
fi

if [ $1 = "wai" ];
	then
		create_wai_subscriptions
		exit 0
fi

if [ $1 = "all" ];
	then
		create_drone_ue
		create_location_subscriptions
		create_rni_subscriptions
		create_wai_subscriptions
		exit 0
fi

