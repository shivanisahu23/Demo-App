frappe.ui.form.on("Purchase Order", {
    refresh: function(frm){
        calculate_total(frm)
    }
})

frappe.ui.form.on('Purchase Order Item', {
    rate: function(frm, cdt, cdn) {
        // console.log("frm, cdt, cdn",cdn);
        
        calculate_total(frm);
    },
    qty: function(frm, cdt, cdn) {
        calculate_total(frm);
    },
    amount: function(frm, cdt, cdn) {
        calculate_total(frm)
    },
    custom_discount: function(frm, cdt, cdn) {
        calculate_total(frm)
    }
    
});
function calculate_total(frm) {
    let total = 0;

    frm.doc.items.forEach(r => {
        if (r.rate && r.qty) {
            r.amount = (r.rate * r.qty) * (1 - r.custom_discount / 100);
            total += r.amount;
        }
    });
    frm.refresh_field('items');
    frm.set_value('total', total);
}

