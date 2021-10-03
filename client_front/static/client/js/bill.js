


const bills = document.querySelectorAll('.bills');


const viewBill = (id_bill) => {
    
}



bills.forEach(bill => {
    bill.addEventListener('click' (e) => {
        viewBill(Number(e.target.id));
    });
});