import { OrderDetails, OrderMedicineData } from "../lib/datatypes";
import { Button } from "./ui/button";

const OrderListItem = (
    orderDetails : OrderDetails, 
    handleAcceptOrder : (orderID : number) => void,
    handleRemoveOrder : (orderID : number) => void,
    handleOrderViewRequest : (medicineData : OrderMedicineData[]) => void,
) => {
    return (
        <li 
        key={orderDetails.orderId}
        className="px-1 py-2 shadow-md rounded-md border-2 border-gray-300 bg-white flex justify-between items-center mb-2">
            {/* Non-Toggable details */}
            <section className="h-full w-auto px-1">
                <b className="text-red-500">Order ID : <span>{orderDetails.orderId}</span></b>
                <br />
                <b className="text-red-500">Distance : <span>{orderDetails.distance}km</span></b>
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
                {/* Acceptance & Rejection handling */}
                <section className="h-full w-auto flex gap-1">
                    <Button 
                    onClick={() => handleAcceptOrder(orderDetails.orderId)}
                    className="bg-green-500 text-white">
                        ✔Accept Order
                    </Button>

                    <Button
                    onClick={() => handleRemoveOrder(orderDetails.orderId)}
                    className="bg-red-500 text-white">
                        🗑Remove Order
                    </Button>
                </section>
            </section>
        </li>
    );
}
 
export default OrderListItem;