import { memo } from "react";
import { OrderMedicineData } from "../lib/datatypes";
import { Button } from "./ui/button";

const MedicineListModal = memo((
    { 
        medicineData,
        handleModalCloseRequest
    } : { 
        medicineData : OrderMedicineData[];
        handleModalCloseRequest : () => void;
    }
) => {
    return (
        <section className="absolute z-50 h-full w-1/2 overflow-hidden bg-white top-0 right-0 shadow-lg">
            {/* Header */}
            <h2
            className="p-2 font-bold text-xl bg-green-200">
                Ordered Medicines List
            </h2>

            {/* Medicine List Section */}
            <section
            className="h-[calc(100%-44px-64px)] w-full p-2">
                <ul
                className="h-full w-full border border-black rounded-lg overflow-x-hidden overflow-y-auto p-2">
                    {
                        medicineData.map((item, index) => (
                            <li
                            key={index}
                            className="w-full p-4 flex justify-between bg-gray-200 rounded-2xl mb-2">
                                <b>
                                    { item.medicineName }
                                </b>
                                <b>
                                    Quantity : { item.medicineQuantity }
                                </b>
                            </li>
                        ))
                    }
                </ul>
            </section>

            {/* Close event section */}
            <section 
            className="h-16 w-full overflow-hidden bg-red-200 flex justify-start items-center p-2">
                <Button 
                onClick={_ => handleModalCloseRequest()
                }
                className="bg-red-500 active:bg-red-700 hover:bg-red-600">
                    Close
                </Button>
            </section>
        </section>
    );
});
 
export default MedicineListModal;