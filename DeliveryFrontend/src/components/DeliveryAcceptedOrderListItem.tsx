import { toast } from "sonner";
import apiFetcher from "../lib/apiFetcher";
import { AcceptedOrderDetails, OrderMedicineData } from "../lib/datatypes";
import { Button } from "./ui/button";

const DeliveryAcceptedOrderListItem = (
    orderDetails : AcceptedOrderDetails,
    handleOrderViewRequest : (medicineData : OrderMedicineData[]) => void,
    handleOrderDeliveryHandOver : (orderId : number) => void,
    handleRejectOrder : (orderId : number) => void,
    verfiedOrder : boolean = false
) => {
    return (
        <li 
        key={orderDetails.orderId}
        className="px-1 py-2 shadow-md rounded-md border-2 border-gray-300 bg-white flex justify-between items-center mb-2">
            {/* Non-Toggable details */}
            <section className="h-full w-auto px-1">
                <b className="text-red-500">
                    Order ID : <span>
                            {orderDetails.orderId}
                        </span> | Token : <span>
                            {orderDetails.orderToken}
                        </span>
                </b>
                <b className="size-auto px-1">
                    {
                        verfiedOrder? 
                        <span className="inline-block px-1 bg-green-500 text-white rounded-full">Verified</span>:
                        <span className="inline-block px-1 bg-yellow-500 text-black rounded-full">Not Verified</span>
                    }
                </b>
                <br />
                <b className="text-red-500">
                    Distance : <span>
                            {orderDetails.distance}km
                        </span>
                </b>
            </section>
            
            {/* Clickables */}
            <section className="h-full w-auto flex justify-center items-center gap-1">
                {/* Toggable details */}
                <section className="h-full w-auto flex gap-1">
                    {/* Location Details */}
                    <section className="inline-block">
                        <a href={orderDetails.locationLink} target="_blank">
                            <Button>
                                📍View Location
                            </Button>
                        </a>
                    </section>
                
                    {/* Medicine Details */}
                    <section className="inline-block">
                        <Button
                        onClick={() => handleOrderViewRequest(orderDetails.medicineData)}>
                            🛒View Orders
                        </Button>
                    </section>
                </section>
                {/* Handover & Rejection handling */}
                <section className="h-full w-auto flex gap-1">
                    <Button
                    onClick={() => {
                        apiFetcher.deliverySignal(orderDetails.orderId)
                            .then(res => {
                                if(res.ok) {
                                    handleOrderDeliveryHandOver(orderDetails.orderId);
                                }
                            })
                            .catch(err => {
                                toast(
                                    <span className="text-red-500 font-bold">
                                        Couldn't send signal
                                        {err}
                                    </span>
                                );
                            })
                    }}
                    className="bg-green-500 text-white">
                        Hand Over
                    </Button>

                    
                    <Button
                    onClick={() => handleRejectOrder(orderDetails.orderId)}
                    className="bg-red-500 text-white">
                        ❌Reject Order
                    </Button>
                </section>
            </section>
        </li>
    );
}
 
export default DeliveryAcceptedOrderListItem;