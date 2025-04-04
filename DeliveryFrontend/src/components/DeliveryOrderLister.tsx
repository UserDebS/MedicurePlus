import { useEffect, useRef, useState } from "react";
import { useAuth } from "../lib/authContext";
import MedicineListModal from "./MedicineListModal";
import { RealtimeChannel, RealtimePostgresChangesPayload, RealtimePostgresUpdatePayload } from "@supabase/supabase-js";
import { LinkedList } from "../lib/dataStructures";
import { DeliveryAcceptedOrderDetails, OrderDetails, OrderMedicineData } from "../lib/datatypes";
import { toast } from "sonner";
import OrderListItem from "./OrderListItem";
import { deliveryChannelSubscription, getOrderLocation } from "../lib/supabaseClient";
import apiFetcher from "../lib/apiFetcher";
import DeliveryAcceptedOrderListItem from "./DeliveryAcceptedOrderListItem";
import distance from "../lib/distance";
import Modal from "./Modal";

const DeliveryOrderLister = () => {
    const {deliveryValidated} = useAuth();
    const [locationPermission, setLocationPermission] = useState<boolean>(false);
    const [hide, setHide] = useState<boolean>(true);

    const [modalHide, setModalHide] = useState<boolean>(true);
    const [currentOrderId, setCurrentOrderId] = useState<number>(-1);

    // Channel Reference
    const deliveryChannelRef = useRef<RealtimeChannel | null>(null);

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
    const [acceptedOrders, setAcceptedOrders] = useState<DeliveryAcceptedOrderDetails[]>([]);

    const handleLocationPermission = () => {
        window.navigator.permissions
        .query({name : 'geolocation'})
        .then(permissionStatus => {
            setLocationPermission(permissionStatus.state === 'granted');
            if(!(permissionStatus.state === 'granted')) toast(
                <span className="text-red-500 font-bold">
                    Enable location to place order!
                </span>
            );

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
                    else throw new Error('Could not fetch Accepted Order Details');
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

        if(deliveryChannelRef.current === null) {
            getOrderedMedicineDataColdStart();
            getAcceptedMedicineDataColdStart();

            console.log('Setting up channel');

            deliveryChannelRef.current = deliveryChannelSubscription(
                // Order Queue
                (payload : RealtimePostgresUpdatePayload<{[key : string] : any}>) => {
                    console.log(payload);
                    if(payload.new.status === 'ONTHEWAY') {
                        setAcceptedOrders(prevOrders =>
                            [
                                ...prevOrders.map(orders => 
                                    orders.orderId === payload.new.id
                                    ? { ...orders, verified : true }
                                    : orders
                                )
                            ]
                        );
                    }
                },
                // Order To Delivery
                (payload : RealtimePostgresChangesPayload<{[key : string] : any}>) => {
                    if(payload.eventType === 'INSERT') {
                        setFrontOrderList(prevList => {
                            const newList = prevList.copy();

                            newList.deleteData({
                                orderId : payload.new.order_id,
                                distance : -1,
                                medicineData : [],
                                locationLink : ''
                            });

                            return newList;
                        });

                        setBackOrderList(prevList => {
                            const newList = prevList.copy();

                            newList.deleteData({
                                orderId : payload.new.order_id,
                                distance : -1,
                                medicineData : [],
                                locationLink : ''
                            });

                            return newList;
                        });
                    }
                },
                // Order To Shop
                (payload : RealtimePostgresChangesPayload<{[key : string] : any}>) => {
                   if(payload.eventType === 'INSERT') {
                        
                        window.navigator.geolocation.getCurrentPosition(location => {
                            getOrderLocation(payload.new.order_id)
                                .then(res => {
                                    const { latitude, longitude } = res;
                                    const dist = distance(
                                        location.coords.latitude,
                                        location.coords.longitude,
                                        latitude,
                                        longitude
                                    );

                                    if(dist <= 8) {
                                        apiFetcher.getDeliveryMedicineData(
                                            payload.new.shop_id,
                                            payload.new.order_id
                                        ).then(res => {
                                            if(res.ok) return res.json();
                                            else throw new Error('Order could not be loaded');
                                        })
                                        .then(res => {
                                            setBackOrderList(prevList => {
                                                const newBackList = prevList.copy();

                                                newBackList.addData({
                                                    orderId : payload.new.order_id,
                                                    distance : dist,
                                                    medicineData : res,
                                                    locationLink : `https://www.google.com/maps/dir/${location.coords.latitude},${location.coords.longitude}/${latitude},${longitude}`
                                                });

                                                return newBackList;
                                            });
                                        })
                                        .catch(err => {
                                            toast(
                                                <span>
                                                    Order could not be loaded
                                                    {err}
                                                </span>
                                            );
                                        })
                                    }
                                })
                                .catch(err => {
                                    toast(
                                        <span className="text-red-500 font-bold">
                                            Couldn't get order location
                                            {err}
                                        </span>
                                    )
                                });
                        });

                   } else if(payload.eventType === 'DELETE') {
                        setFrontOrderList(prevList => {
                            const newList = prevList.copy();

                            newList.deleteData({
                                orderId : payload.old.order_id,
                                distance : -1,
                                medicineData : [],
                                locationLink : ''
                            });

                            return newList;
                        });

                        setBackOrderList(prevList => {
                            const newList = prevList.copy();

                            newList.deleteData({
                                orderId : payload.old.order_id,
                                distance : -1,
                                medicineData : [],
                                locationLink : ''
                            });

                            return newList;
                        });

                        setAcceptedOrders(prevList => [...prevList.filter(item => item.orderId !== payload.old.order_id)]);
                   }
                }
            );
        }
    }, [locationPermission, deliveryValidated]);

    const handleOrderViewRequest = (medicineData : OrderMedicineData[]) => {
        setMedicinedata(medicineData);
        setHide(false);
    }

    const handleRemoveOrder = (orderId : number) => {
        setFrontOrderList(prevFrontList => {
            const newFrontList = prevFrontList.copy();

            newFrontList.deleteData({
                orderId : orderId,
                distance : 0,
                locationLink : '',
                medicineData : []
            });

            if(newFrontList.getSize() === 0) {
                setBackOrderList(prevBackList => {
                    const newBackList = prevBackList.copy();

                    newFrontList.insertDataFromList(newBackList, 10);

                    return newBackList;
                });
            }

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
    
                    setAcceptedOrders(prevOrders => [...prevOrders, {...data, orderToken : res.order_token, verified : false}]);
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
            .catch(err => {
                toast(
                    <span>
                        Couldn't reject order <br />
                        {err}
                    </span>
                );
            });
    }

    const handleOrderDeliveryHandOver = (orderId : number, orderToken : string) => {
        apiFetcher.deliveryHandOver(orderId, orderToken)
                    .then(res => {
                        if(res.ok) return res.json();
                        else throw new Error('Unsuccessful handover');
                    })
                    .then(res => {
                        if(res.status === 201) {
                            setAcceptedOrders(prevOrders => [...prevOrders.filter(item => item.orderId !== orderId)]);
                            toast(
                                <span className="text-green-500 font-bold">
                                    Successful Handover!
                                </span>
                            );
                        }
                        else throw new Error('Unsuccessful handover');
                    })
                    .catch(err => {
                        toast(
                            <span className="text-red-500 font-bold">
                                Unsuccessful Handover!
                                {err}
                            </span>
                        );
                    });
    }

    return ( 
        <div className="h-full w-full overflow-hidden py-1 relative">
            {
                modalHide
                ? <></>
                : <Modal 
                    orderId={currentOrderId}
                    closeHandler={() => {
                        setModalHide(true);
                    }}
                    handOverHandler={handleOrderDeliveryHandOver}
                />
            }
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
                                acceptedOrders.map(item => DeliveryAcceptedOrderListItem(
                                        item,
                                        handleOrderViewRequest,
                                        (orderId : number) => {
                                            setCurrentOrderId(orderId);
                                            setModalHide(false);
                                        },
                                        handleRejectOrder,
                                        item.verified
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