/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { FormController } from "@web/views/form/form_controller";
import { patch } from  "@web/core/utils/patch";

patch(FormController.prototype, 'ark_dotmatrix.form_controller', {
    setup() {
        this._super(...arguments)
        this.orm = useService("orm");
        this.action = useService("action");
    },
    async beforeExecuteActionButton(clickParams) {
        var url = "http://localhost:5000"
        if (clickParams.name === "print_button"){
            // var print_data = this.model.root.data.print_data;
            const print_data = await this.orm.call(
                this.props.resModel,
                "get_data",
                [this.props.resId],
                {}
                );
            // if (!print_data){
            //     alert('No Data');
            //     return;
            // }
            console.log(print_data)
            
            await $.ajax({
                type: "POST",
                contentType: "application/json; charset=utf-8",
                dataType: "text",
                url: url,
                data: JSON.stringify(print_data
                ),
                success: async function(data) {
                    console.log('Success');
                    console.log(data);
                },
                error: function(data){
                    console.log('Failed');
                    console.log(data);
                },
            })
        }
        // if (clickParams.name === 'action_allow_reprint') {
            // const print_data = await this.orm.call(
            //     this.props.resModel,
            //     "get_print_data",
            //     [this.props.resId, this.props.resModel, this.props.resId],
            //     {}
            //     );

            // await $.ajax({
            //     type : "POST",
            //     contentType: "application/json; charset=utf-8",
            //     dataType: "text",
            //     url : "http://localhost:5000",
            //     data : JSON.stringify(print_data),
            //     success : async (text_data) => {
            //         if (text_data) {
            //             var parsed_data = JSON.parse(text_data.slice(1,-1));
            //             if (parsed_data.success === true) {
            //                 const set_success = await this.orm.call(
            //                     this.props.resModel,
            //                     'set_print_success',
            //                     [this.props.resId, this.props.resModel, this.props.resId ],
            //                     {});
            //                 console.log('Print Berhasil')
            //             } else {
            //                 console.log(parsed_data.messages)
            //                 alert(parsed_data.messages);
            //             }
            //         } else {
            //             console.log(failed_printer)
            //             alert(failed_printer);
            //         }
            //     },
            //     error : (text_data) => {
            //         console.log(failed_printer)
            //         alert(failed_printer);
            //     },
            // });

            // try {
            //     return this._super(...arguments);
            // } catch (error) {
            //     console.log(error);
            // }
            
        // }
        else {
            return this._super(...arguments);
        }
    }
})