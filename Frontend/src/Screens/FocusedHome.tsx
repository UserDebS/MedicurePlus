import Med_Card from "@/components/Card";
import GridShowcase from "@/components/ui/GridShowcase";
import apiFetcher from "@/lib/apiFetcher";
import { MedicineDetailedData } from "@/lib/datatypes";
import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { useCart } from "@/components/Cart";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const FocusedHome = () => {
    const [medicine, setMedicine] = useState<MedicineDetailedData>();
    const [loading, setLoading] = useState(true);
    const [offset, setOffset] = useState<number>(0);
    const [quantity, setQuantity] = useState<number>(0);
    const { dispatch } = useCart();
    const { id } = useParams();
    const totalPrice: number = quantity * medicine?.data.cost!;

    const fetchData = async () => {
        await apiFetcher.getMedicineByID(Number.parseInt(id!.toString()), offset, 20).then(async (res) => {
            const data = await res.json();
            setMedicine(data);
        }).catch(_ => console.log(_)).finally(() => setLoading(false));
    }

    const fetchRecommendation = async() => {
        await apiFetcher.getRecommendedListByID(Number.parseInt(id!.toString()), offset, 20)
        .then(async (res) => {
            const data = await res.json();
            setMedicine(prev => {
                if(prev !== undefined) {
                    return {
                        data : prev.data,
                        recommendation : [...prev.recommendation, ...data]
                    };
                }
            })
        })
    }

    const handleChange: React.ChangeEventHandler<HTMLInputElement> = (e) => {
        if (e.target.value == '') {
            setQuantity(0);
            return;
        }
        setQuantity(Number.parseInt(e.target.value))
    }

    const addCart = () => {
        if (quantity === 0) return;
        if (medicine?.data.name === undefined) return;

        dispatch({
            type: 'ADD',
            payload: {
                key: medicine?.data.name,
                cost: medicine.data.cost,
                quantity: quantity
            }
        })
    }

    useEffect(() => {
        fetchData()
    }, [id]);

    useEffect(() => {
        fetchRecommendation();
    }, [offset])

    return (loading ?
        <div className="h-full w-full flex justify-center items-center"><span className="inline-block text-xl font-bold">Loading...</span></div> :
        <div className="h-full w-full flex justify-center items-center">
            <div className="details w-3/4 h-full p-3">
                <div className="w-full h-1/3 flex justify-between items-center overflow-hidden">
                    <img
                        title={medicine?.data.name}
                        className="h-full w-1/2 rounded-sm"
                        src={medicine?.data.image!}
                        alt={medicine?.data.name} />

                    <div className="h-full w-1/2 px-1">
                        <h1 title={medicine?.data.name} className="font-bold text-3xl mb-2">{medicine?.data.name}</h1>

                        <p className={"inline-block px-2 rounded-full font-bold text-white " + (
                            (medicine?.data.available) ? "bg-green-500" : "bg-red-500"
                        )}>{medicine?.data.available ? "Availble" : "Not Available"}</p>

                        <p className="mb-1 font-bold text-2xl">Cost : <span title={medicine?.data.cost.toString()} className="text-green-500">₹{medicine?.data.cost}</span></p>

                        <p className="font-bold block mb-1 text-lg">Total Price</p>

                        <p className="font-bold block text-xl text-green-500">₹{totalPrice.toFixed(2)}</p>

                        <label htmlFor={medicine?.data.name + "quantity"} className="font-bold block mb-2">Quantity</label>

                        <Input onChange={handleChange} value={quantity} id={medicine?.data.name + "quantity"} type="text" className="w-1/2 inline-block" />

                        <Button onClick={addCart} className="ml-2 h-[calc(26.222px+8px+2*0.889px)]">Add to Cart</Button>
                    </div>
                </div>
                <div className="w-full h-full p-1">
                    <section id="medical_condition">
                        <h3 className="text-lg font-bold">Medical Conditions</h3>
                        <div className="w-full h-10 flex justify-start items-start gap-1 p-1 flex-wrap">
                            {
                                medicine?.data.medical_conditions.map(item => <span className="inline-block h-full px-2 py-1 rounded-full bg-green-400 font-bold text-white">{item}</span>)
                            }
                        </div>
                    </section>
                    <section id="active-ingredient">
                        <h3 className="text-lg font-bold">Active Ingredients</h3>
                        <div className="w-full h-10 flex justify-start items-start gap-1 p-1 flex-wrap">
                            {
                                medicine?.data.active_ingredients.map(item => <span className="inline-block h-full px-2 py-1 rounded-full bg-green-400 font-bold text-white">{item}</span>)
                            }
                        </div>
                    </section>
                    <section id="dosage_form">
                        <h3 className="text-lg font-bold">Dosage Forms</h3>
                        <div className="w-full h-10 flex justify-start items-start gap-1 p-1 flex-wrap">
                            {
                                medicine?.data.dosage_forms.map(item => <span className="inline-block h-full px-2 py-1 rounded-full bg-green-400 font-bold text-white">{item}</span>)
                            }
                        </div>
                    </section>
                    <section id="side_effect">
                        <h3 className="text-lg font-bold">Side Effects</h3>
                        <div className="w-full h-10 flex justify-start items-start gap-1 p-1 flex-wrap">
                            {
                                medicine?.data.side_effects.map(item => <span className="inline-block h-full px-2 py-1 rounded-full bg-green-400 font-bold text-white">{item}</span>)
                            }
                        </div>
                    </section>
                    <section id="brand_name">
                        <h3 className="text-lg font-bold">Brand Names</h3>
                        <div className="w-full h-10 flex justify-start items-start gap-1 p-1 flex-wrap">
                            {
                                medicine?.data.brand_names.map(item => <span className="inline-block h-full px-2 py-1 rounded-full bg-green-400 font-bold text-white">{item}</span>)
                            }
                        </div>
                    </section>

                </div>
            </div>
            <div className="w-2/3 h-full">
                <GridShowcase setOffset={setOffset}>
                    {
                        medicine?.recommendation.map(data => <Med_Card
                            image={data.image}
                            name={data.name}
                            cost={data.cost}
                            available={data.available}
                            self_url={data.self_url}
                        />)
                    }
                </GridShowcase>
            </div>
        </div>
    );
}

export default FocusedHome;