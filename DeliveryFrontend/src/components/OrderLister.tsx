import { useEffect, useRef, useState } from "react";
import { Button } from "./ui/button";
import { LinkedList } from "../lib/dataStructures";
import { subscribeChannel } from "../lib/supabaseClient";
import { RealtimeChannel } from "@supabase/supabase-js";
import { toast } from "sonner";
import distance from "../lib/distance";
import apiFetcher from "../lib/apiFetcher";
import { OrderDetails, OrderMedicineData } from "../lib/datatypes";

const OrderLister = () => {
    const channelRef = useRef<RealtimeChannel | null>(null);
    const [frontOrderList, setFrontOrderList] = useState<LinkedList<OrderDetails>>(new LinkedList<OrderDetails>(
        (a : OrderDetails, b : OrderDetails) => a.orderId === b.orderId,
        (listElement : OrderDetails, insertingElement : OrderDetails) => (listElement.distance < insertingElement.distance)? -1 :
        (listElement.distance === insertingElement.distance)? 0 :
        1
    ));

    const [backOrderList, setBackOrderList] = useState<LinkedList<OrderDetails>>(new LinkedList<OrderDetails>(
        (a : OrderDetails, b : OrderDetails) => a.orderId === b.orderId,
        (listElement : OrderDetails, insertingElement : OrderDetails) => (listElement.distance < insertingElement.distance)? -1 :
        (listElement.distance === insertingElement.distance)? 0 :
        1
    ));

    const [acceptedOrders, setAcceptedOrders] = useState<OrderDetails[]>([]);

    const [locationPermission, setLocationPermission] = useState<boolean>(false);

    const handleLocationPermission = () => {
        window.navigator.permissions
        .query({name : 'geolocation'})
        .then(permissionStatus => {
            setLocationPermission(permissionStatus.state === 'granted');
            if(!(permissionStatus.state === 'granted')) toast(
                <span className="text-red-500 font-bold">
                    Enable location to place order!
                </span>
            )

            permissionStatus.onchange = () => {
                if(permissionStatus.state === 'granted') setLocationPermission(true);
                else setLocationPermission(false);   
            }
        })
        .catch(_ => {
            toast(
                <span className="text-red-500 font-bold">
                    Could't read permission status!
                </span>
            )
        })
    }

    useEffect(() => {
        handleLocationPermission();
    }, []);

    useEffect(() => {
        if(!locationPermission) return;

        const getOrderedMedicineDataColdStart = async() => {
            await apiFetcher.getOrders()
                .then(async (res) => {
                    const data : OrderDetails[] = await res.json();
                    const newFrontList = frontOrderList.copy();
    
                    data.forEach(item => {
                        newFrontList.addData(item);
                    });
    
                    setFrontOrderList(newFrontList);
                })
                .catch(err => {
                    toast(
                        <span className="text-red-500 font-bold">
                            Couldn't get <em>orders</em>!
                            {err}
                        </span>
                    )
                })
        };

        if(channelRef.current === null) {
            getOrderedMedicineDataColdStart();
            console.log('Setting up channel');
            channelRef.current = subscribeChannel(
                'order_queue',
                (payload : any) => {
                    payload = payload.new;

                    window.navigator.geolocation.getCurrentPosition(location => {
                        const dist : number = distance(
                            payload.latitude as number, 
                            payload.longitude as number, 
                            location.coords.latitude,
                            location.coords.longitude
                        );
                        if(dist <= 8 && payload.status === 'PENDING') {
                            (async() => {
                                const newBackOrderList : LinkedList<OrderDetails> = backOrderList.copy();

                                newBackOrderList.addData({
                                    orderId : payload.id,
                                    distance : dist,
                                    locationLink : 'user defined',
                                    medicineData : await apiFetcher.getOrderMedicineData(payload)
                                    .then(async(res) => {
                                        const data : OrderMedicineData[] = await res.json();
                                        return data;
                                    })
                                    .catch(_ => [])
                                })

                                setBackOrderList(newBackOrderList);
                            })()
                        }
                    }, err => {
                        toast(
                            <span className="text-red-500 font-bold">
                                Couldn't access <em>Location Details</em>! <br />
                                {err.message}
                            </span>
                        )
                        }
                    );
                },
                (payload : any) => {
                    payload = payload.new;

                    window.navigator.geolocation.getCurrentPosition(location => {
                        const dist : number = distance(
                            payload.latitude as number, 
                            payload.longitude as number, 
                            location.coords.latitude,
                            location.coords.longitude
                        );

                        const newFrontList = frontOrderList.copy();
                        const newBackList = backOrderList.copy();

                        if(dist > 8 || payload.status !== 'PENDING') {
                            newFrontList.deleteData({
                                orderId : payload.id,
                                distance : dist,
                                locationLink : '',
                                medicineData : []
                            });

                            newBackList.deleteData({
                                orderId : payload.id,
                                distance : dist,
                                locationLink : '',
                                medicineData : []
                            });

                            if(newFrontList.getSize() === 0) newFrontList.insertDataFromList(newBackList, 15); 

                        } else {
                            (async() => {
                                const data : OrderMedicineData[] = await apiFetcher.getOrderMedicineData(payload.id)
                                    .then(async(res) => {
                                        const result : OrderMedicineData[] = await res.json();
                                        return result;
                                    })
                                    .catch(_ => []);

                                newFrontList.updateData({
                                    orderId : payload.id,
                                    distance : dist,
                                    locationLink : 'user defined',
                                    medicineData : data
                                });

                                newBackList.updateData({
                                    orderId : payload.id,
                                    distance : dist,
                                    locationLink : 'user defined',
                                    medicineData : data
                                });
                            })();
                        }

                        setFrontOrderList(newFrontList);
                        setBackOrderList(newBackList);

                    }, err => {
                            toast(
                                <span className="text-red-500 font-bold">
                                    Couldn't access <em>Location Details</em>! <br />
                                    {err.message}
                                </span>
                            );
                        }
                    );
                }
            );
        }
    }, [locationPermission]);

    const handleAcceptOrder = async (orderId : number) => {
        await apiFetcher.acceptOrder(orderId)  
        .then(res => {
            
        })
        .catch(err => toast(
            <span>
                Couldn't accept order
            </span>
        ))
    }

    const handleRejectOrder = async (orderId : number) => {
        await apiFetcher.acceptOrder(orderId)  
        .then(res => {
            
        })
        .catch(err => toast(
            <span>
                Couldn't accept order
            </span>
        ))
    }

    return ( 
        <div className="h-full w-full overflow-x-hidden overflow-y-auto">
            {
                !locationPermission? 
                <div className="h-full w-full flex justify-center items-center">
                    <strong>Location permission</strong> is not given
                </div> :
                <>
                <section className="h-1/2">
                    <h1 className="capitalize">Pending orders</h1>
                    <ul className="block w-full max-h-">
                        {
                            
                        }
                    </ul>
                </section>
                <section className="h-1/2">
                    <h1 className="capitalize">Accepted orders</h1>
                    <ul>

                    </ul>
                </section>
                </>

            }
        </div>
    );
}
 
export default OrderLister;