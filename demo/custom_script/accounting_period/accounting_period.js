frappe.ui.form.on("Accounting Period", {
    custom_fiscal_year: function(frm) {
        maybe_set_period_dates(frm);
    },
    custom_month: function(frm) {
        maybe_set_period_dates(frm);
    }
});

function maybe_set_period_dates(frm) {
    if (frm.doc.custom_fiscal_year && frm.doc.custom_month) {
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Fiscal Year",
                name: frm.doc.custom_fiscal_year
            },
            callback: function(r) {
                if (r.message) {
                    let fiscal_start = frappe.datetime.str_to_obj(r.message.year_start_date);
                    let fiscal_end = frappe.datetime.str_to_obj(r.message.year_end_date);
                    let month_name = frm.doc.custom_month;

                    const months = [
                        "January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"
                    ];
                    let month_index = months.indexOf(month_name);
                    if (month_index === -1) return;

                    let fiscal_start_year = fiscal_start.getFullYear();
                    let fiscal_end_year = fiscal_end.getFullYear();

                    let target_year = (month_index < 3) ? fiscal_end_year : fiscal_start_year;

                    let start_date = new Date(target_year, month_index, 1);

                    let end_day;
                    if (month_index === 1) { 
                        end_day = (is_leap_year(target_year)) ? 29 : 28;
                    } else if ([3, 5, 8, 10].includes(month_index)) {
                        end_day = 30;
                    } else {
                        end_day = 31;
                    }

                    let end_date = new Date(target_year, month_index, end_day);

                    frm.set_value("start_date", frappe.datetime.obj_to_str(start_date));
                    frm.set_value("end_date", frappe.datetime.obj_to_str(end_date));
                }
            }
        });
    }
}

function is_leap_year(year) {
    return ((year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0));
}

// frappe.ui.form.on("Accounting Period", {
//     refresh(frm) {

//     }
// })

// frappe.ui.form.on("Monthly Input", {
// 	refresh(frm) {
//         frm.disable_save();
// 	},
//     click_here:function(frm){
//         frappe.call({
//             method:"airplanemode.airplane_mode.doctype.monthly_input.monthly_input.get_value",
//             args: {
//                 name1 :frm.doc.name1,
//                 amount: frm.doc.amount,
//                 fiscal_year: frm.doc.fiscal_year,
//                 month: frm.doc.month
//             },


//         })
//         // console.log(frm.doc.amount)

        
//     }
    
// });