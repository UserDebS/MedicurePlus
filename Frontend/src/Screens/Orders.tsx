import apiFetcher from "@/lib/apiFetcher";
import { useEffect, useState } from "react";

const Orders = () => {
    interface sublist {
        name : string;
        cost : number;
        quantity : number
    }

    interface orderlist {
        total : number;
        placed : string;
        orders : sublist[]
    }
    const [orders, setOrders] = useState<orderlist[]>([]);
    const [loading, setLoading] = useState(true);


    const fetchOrderData = async () => {
        await apiFetcher.getOrders(0, 100).then(async(res) => {
            if (res.status == 200) {
                const data = await res.json();
                console.log(data)
                setOrders(data);
            }
        }).catch(_ => console.log(_)).finally(() => { setLoading(false) })
    };

    useEffect(() => {
        fetchOrderData();
        console.log(orders)
    }, []);

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 py-8">
            <h1 className="text-2xl font-bold mb-6">Order List</h1>
            <div className="w-full max-w-2xl px-4">
                {loading ? (
                    <p className="text-center text-gray-500">Loading...</p>
                ) : orders.length > 0 ? (
                    orders.map((order, index) => (
                        <div
                            key={index}
                            className="bg-white shadow-md rounded-lg p-4 mb-6"
                        >
                            <div className="mb-4">
                                <h2 className="text-lg font-semibold">
                                    Order Placed: {order.placed}
                                </h2>
                                <p className="text-gray-500">Total: ${order.total.toFixed(2)}</p>
                            </div>
                            <div className="divide-y">
                                {order.orders.map((item, idx) => (
                                    <div key={idx} className="py-2 flex justify-between">
                                        <div>
                                            <h3 className="text-md font-medium">{item.name}</h3>
                                            <p className="text-gray-500">
                                                Quantity: {item.quantity}
                                            </p>
                                        </div>
                                        <p className="text-gray-700">${item.cost.toFixed(2)}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))
                ) : (
                    <p className="text-center text-gray-500">No orders found</p>
                )}
            </div>
        </div>
    );
}

export default Orders;