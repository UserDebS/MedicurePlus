import Med_Card from "@/components/ui/Card";
import apiFetcher from "@/lib/apiFetcher";
import { MedicineDetailedData } from "@/lib/datatypes";
import { useEffect, useState } from "react";
import { useParams } from "react-router";

const FocusedHome = () => {
    const [medicine, setMedicine] = useState<MedicineDetailedData>();
    const [loading, setLoading] = useState(true);
    const {id} = useParams();

    const fetchData = async() => {
        await apiFetcher.getMedicineByID(Number.parseInt(id!.toString()), 0, 30).then(async(res) => {
            const data = await res.json();
            setMedicine(data);
        }).catch(_ => console.log(_)).finally(() => setLoading(false));
    }
    useEffect(() => {
        fetchData()
    }, [id])
    return ( loading? 
        <div className="h-full w-full justify-center items-center">Loading</div> :
        <div className="h-full w-full flex justify-center items-center">
            <div className="details w-1/2 h-full p-3">
                <h1 className="text-3xl font-bold my-3">{medicine?.data.name}</h1>
                <h2 className="text-2xl font-semibold text-slate-600">₹{medicine?.data.cost}</h2>
                <h2 className="text-2xl font-semibold text-slate-600">{medicine?.data.available? 'Available' : 'Not Available'}</h2>
                <br />
                <strong>Used for : </strong>
                {
                    medicine?.data.medical_conditions.map(data => <span className="border-r-[1px] border-slate-500 mx-2 pr-2">{data}</span>)
                }
                <br />
                <strong>Ingredients used : </strong>
                {
                    medicine?.data.active_ingredients.map(data => <span className="border-r-[1px] border-slate-500 mx-2 pr-2">{data}</span>)
                }
                <br />
                <strong>Dosage forms : </strong>
                {
                    medicine?.data.dosage_forms.map(data => <span className="border-r-[1px] border-slate-500 mx-2 pr-2">{data}</span>)
                }
                <br />
                <strong>Side effects : </strong>
                {
                    medicine?.data.side_effects.map(data => <span className="border-r-[1px] border-slate-500 mx-2 pr-2">{data}</span>)
                }
                <br />
                <strong>Brands available : </strong>
                {
                    medicine?.data.brand_names.map(data => <span className="border-r-[1px] border-slate-500 mx-2 pr-2">{data}</span>)
                }
            </div>
            <div className="similarities w-1/2 h-full flex justify-center items-start p-2 gap-2 flex-wrap">
                {
                    medicine?.recommendation.map(data => <Med_Card 
                        name={data.name} 
                        cost={data.cost} 
                        available={data.available}
                        self_url={data.self_url}
                    />)
                }
            </div>
        </div>
     );
}
 
export default FocusedHome;