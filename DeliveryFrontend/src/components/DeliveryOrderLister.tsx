import { useEffect, useRef, useState } from "react";
import { useAuth } from "../lib/authContext";
import MedicineListModal from "./MedicineListModal";
import { RealtimeChannel } from "@supabase/supabase-js";
import { LinkedList } from "../lib/dataStructures";
import { AcceptedOrderDetails, OrderDetails, OrderMedicineData } from "../lib/datatypes";
import { toast } from "sonner";
import OrderListItem from "./OrderListItem";
import distance from "../lib/distance";
import { subscribeChannel } from "../lib/supabaseClient";
import apiFetcher from "../lib/apiFetcher";

const DeliveryOrderLister = () => {
    const channelRef = useRef<RealtimeChannel | null>(null);
    const {deliveryValidated} = useAuth();
    const [locationPermission, setLocationPermission] = useState<boolean>(false);
    const [hide, setHide] = useState<boolean>(true);

    // UI States
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

    // Fixing state bugs using useRef
    const frontOrderListRef = useRef<LinkedList<OrderDetails>>(frontOrderList);
    const backOrderListRef = useRef<LinkedList<OrderDetails>>(backOrderList);

    const [medicineData, setMedicinedata] = useState<OrderMedicineData[]>([]);
    const [acceptedOrders, setAcceptedOrders] = useState<AcceptedOrderDetails[]>([]);

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
        });
    }

    // Start Up Permission handler
    useEffect(() => {
        handleLocationPermission();
    }, []);


    // State Bug fix
    useEffect(() => {
        frontOrderListRef.current = frontOrderList;
        backOrderListRef.current = backOrderList;
    }, [frontOrderList, backOrderList]);

    // Start Up Set Up
    useEffect(() => {
        if(!locationPermission) return;
        if(!deliveryValidated) return;

        // Load start up pending orders
        const getOrderedMedicineDataColdStart = async() => {
            await apiFetcher.getPendingDeliveryOrders()
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
                });
        };

        // Load start up accepted orders
        const getAcceptedMedicineDataColdStart = async() => {
            await apiFetcher.getAcceptedDeliveryOrders()
                .then(res => {
                    if(res.ok) return res;
                    else throw new Error('Could not fetch Accepted Order Details')
                })
                .then(res => res.json())
                .then(res => {
                    // Set the accepted order list
                    setAcceptedOrders(res);
                })
                .catch(err => {
                    console.log(err);
                    toast(
                        <span className="text-red-500 font-bold">
                            Couldn't get <strong>
                                Accepted Orders
                            </strong> <br />
                            Error : {err}
                        </span>
                    );
                });
        }

        if(channelRef.current === null) {
            getOrderedMedicineDataColdStart();
            getAcceptedMedicineDataColdStart();

            return;
            
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
                                const newBackOrderList : LinkedList<OrderDetails> = backOrderListRef.current.copy();

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
                                });

                                setBackOrderList(newBackOrderList);
                            })();
                        }
                    }, err => {
                            toast(
                                <span className="text-red-500 font-bold">
                                    Couldn't access <em>Location Details</em>! <br />
                                    {err.message}
                                </span>
                            );
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

                        const newFrontList = frontOrderListRef.current.copy();
                        const newBackList = backOrderListRef.current.copy();

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
    }, [locationPermission, deliveryValidated]);

    const handleOrderViewRequest = (medicineData : OrderMedicineData[]) => {
        setMedicinedata(medicineData);
        setHide(false);
    }

    const handleRemoveOrder = (orderId : number) => {
        setFrontOrderList(prevList => {
            const newFrontList = prevList.copy();

            newFrontList.deleteData({
                orderId : orderId,
                distance : 0,
                locationLink : '',
                medicineData : []
            });

            return newFrontList;
        });
    }

    const handleAcceptOrder = async (orderId : number) => {
        await apiFetcher.acceptDeliveryOrder(orderId)
            .then(res => {
                if(res.ok) return res.json();
                else throw new Error('Could not Accept Order');
            })
            .then(res => {
                if(res.status === 200) {
                    // State logic
                    const newFrontList = frontOrderList.copy();
                    const data : OrderDetails | null = newFrontList.deleteData({
                        orderId : orderId,
                        distance : -1,
                        locationLink : '',
                        medicineData : []
                    });
    
                    if(data === null) {
                        throw new Error('Invalid Order');
                    }
    
                    setAcceptedOrders(prevOrders => [...prevOrders, {...data, orderToken : res.order_token}]);
                } else throw new Error('Could not Accept Order');
            })
            .catch(err => toast(
                <span>
                    Couldn't accept order <br />
                    {err}
                </span>
            ));
    }

    const handleRejectOrder = async (orderId : number) => {
        await apiFetcher.rejectDeliveryOrder(orderId)
            .then(res => {
                if(res.ok) return res.json();
                else throw new Error('Order cancellation failed');
            })
            .then(res => {
                if(res.status === 200) {
                    // State logic
                    setAcceptedOrders(prevList => [...prevList.filter(item => item.orderId !== orderId)]);
    
                } else throw new Error('Order cancellation failed');
            })
            .catch(err => toast(
                <span>
                    Couldn't reject order <br />
                    {err}
                </span>
            ));
    }

    return ( 
        <div className="h-full w-full overflow-hidden py-1">
            {
                !hide?
                <MedicineListModal 
                medicineData={medicineData}
                handleModalCloseRequest={() => {
                    setHide(true);
                }}
                /> :
                <></>
            }
            {
                !locationPermission? 
                <div className="h-full w-full flex justify-center items-center">
                    <strong>Location permission</strong> is not given
                </div> :
                <>
                <section className="h-1/2 px-1">
                    <h1 className="capitalize text-3xl py-2 font-bold">Pending orders</h1>
                    <section
                    className="w-full h-[calc(100%-36px-16px)] p-2 border border-black rounded-lg">
                        <ul className="block size-full overflow-y-auto bg-white">
                            {
                                frontOrderList
                                .toList()
                                .map(item => (
                                    OrderListItem({
                                            orderId : item.orderId,
                                            distance : item.distance,
                                            locationLink : item.locationLink,
                                            medicineData : item.medicineData
                                        },
                                        handleAcceptOrder,
                                        handleRemoveOrder,
                                        handleOrderViewRequest
                                    )
                                ))
                            }
                        </ul>
                    </section>
                </section>
                <section className="h-1/2 px-1">
                    <h1 className="capitalize text-3xl py-2 font-bold">Accepted orders</h1>
                    <section
                    className="w-full h-[calc(100%-36px-16px)] p-2 border border-black rounded-lg">
                        <ul className="block size-full bg-white overflow-y-auto">
                            {
                                acceptedOrders.map(item => AcceptedOrderListItem(
                                        item,
                                        handleOrderViewRequest,
                                        handleOrderDeliveryHandOver,
                                        handleRejectOrder
                                    )
                                )
                            }
                        </ul>
                    </section>
                </section>
                </>
            }
        </div>
    );
}
 
export default DeliveryOrderLister;