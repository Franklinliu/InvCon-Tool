package daikon.derive.senary;

import daikon.ProglangType;
import daikon.VarInfo;
import org.checkerframework.checker.nullness.qual.Nullable;

public final class InvConUserBookkeeping2Factory extends SenaryDerivationFactory{

    @Override
    public SenaryDerivation @Nullable [] instantiate(VarInfo vi1, VarInfo vi2, VarInfo vi3, VarInfo vi4, VarInfo vi5, VarInfo vi6) {
        // TODO Auto-generated method stub

        boolean enable_bookkeeping = InvConUserBookkeeping2.dkconfig_enabled;
        if (!enable_bookkeeping) {
            return null;
        }

        // System.out.print("userbookkeeping2 factory testing start");

        VarInfo[] vis = new VarInfo[]{vi1, vi2, vi3, vi4, vi5, vi6};
        
        // mapping(address => mapping(address => uint)) allowed.
        // String[] this.allowed[]
        // String[] this.allowed[].getSub_key()
        // int[] this.allowed[].getSubLength()
        // double[] this.allowed[].getSubValue()
        // String key_var1 (spender)
        // String key_var2 (msg.sender)
        // enclosing var
        VarInfo main_keys_var = null ; 
        // child vars
        VarInfo sub_keys_var = null;
        VarInfo sub_lengths_var = null;
        VarInfo values_var = null;
        // key vars
        // it's hard to figure out what is main key or subordinary key
        // using only the variable information.
        // we kept this for runtime checking
        // VarInfo main_key_var;
        // VarInfo sub_key_var;
        VarInfo key_var1 = null ;
        VarInfo key_var2 = null ;

        VarInfo[] String_Arrays = new VarInfo[2];
        int String_Arrays_cnt = 0;
        VarInfo Int_Array = null;
        VarInfo Double_Array = null;
        VarInfo[] String_Vars = new VarInfo[2];
        int String_Vars_cnt = 0 ;
        // System.out.println(vis);
        for (VarInfo vi: vis){
            if (vi.rep_type == ProglangType.STRING_ARRAY){
                if (String_Arrays_cnt == 2){
                    return null;
                }
                String_Arrays[String_Arrays_cnt] = vi;
                String_Arrays_cnt++;
            }else if (vi.rep_type == ProglangType.DOUBLE_ARRAY){
                Double_Array = vi;
            }else if (vi.rep_type == ProglangType.BIGINT_ARRAY){
                Double_Array = vi;
            }else if (vi.rep_type ==  ProglangType.INT_ARRAY){
                Int_Array = vi;
            }else if (vi.rep_type== ProglangType.STRING){
                if (String_Vars_cnt == 2){
                    return null;
                }
                String_Vars[String_Vars_cnt] = vi;
                String_Vars_cnt++;
            }
        }

        // System.out.println(String_Arrays);
        // System.out.println(String_Vars);
        // System.out.println(Int_Array);
        // System.out.println(Double_Array);
        // System.out.println("userbookkeeping2 factory testing 0");

        if (!(String_Arrays_cnt == 2 
        && String_Vars_cnt == 2 
        && Int_Array!=null 
        && (Double_Array!=null)
        && String_Vars[0]!=null 
        && String_Vars[1]!=null
        )){
            return null;
        }

        // System.out.println("userbookkeeping2 factory testing 1");
        // System.out.println("String_Arrays[0].name(): "+ String_Arrays[0].name());
        // System.out.println("String_Arrays[1].name(): "+String_Arrays[1].name());
    
        if (String_Arrays[0].get_enclosing_var()!=null){
            // System.out.printf("(%s==%s: %b\n", String_Arrays[0].get_enclosing_var().name(), 
            // String_Arrays[1].name(), String_Arrays[0].get_enclosing_var().name().equals(String_Arrays[1].name()));
            if (String_Arrays[0].get_enclosing_var().name().equals(String_Arrays[1].name())){
                main_keys_var  = String_Arrays[1];
                sub_keys_var = String_Arrays[0];    
            }
        }
        
        if (String_Arrays[1].get_enclosing_var()!=null){
            // System.out.printf("(%s==%s: %b\n", String_Arrays[1].get_enclosing_var().name(), 
            // String_Arrays[0].name(), String_Arrays[1].get_enclosing_var().name().equals(String_Arrays[0].name()));
            if (String_Arrays[1].get_enclosing_var().name().equals(String_Arrays[0].name())){
                main_keys_var  = String_Arrays[0];
                sub_keys_var = String_Arrays[1];    
            }
        }

        if (main_keys_var==null || sub_keys_var==null){
            return null;
        }

        // System.out.print("userbookkeeping2 factory testing 2");
        // System.out.printf("Int_Array: %s", Int_Array.name());
        // System.out.printf("Int_Array.get_enclosing_var(): %s", Int_Array.get_enclosing_var().name());
        // System.out.printf("main_keys_var: %s", main_keys_var.name());
        if (Int_Array.get_enclosing_var().name().equals(main_keys_var.name())){
            sub_lengths_var = Int_Array;
        }else{
            return null;
        }

        if (Double_Array!=null){
            // System.out.print("userbookkeeping2 factory testing 3");
            if (Double_Array.get_enclosing_var().name().equals(main_keys_var.name())){
                values_var = Double_Array;
            }else{
                return null;
            }

            // System.out.print("userbookkeeping2 factory testing 4");

            key_var1  = String_Vars[0];
            key_var2 = String_Vars[1];

            if (key_var1.isParam() && key_var2.isParam()){
            return new SenaryDerivation[]{
                new InvConUserBookkeeping2(main_keys_var, sub_keys_var, sub_lengths_var, values_var,
                key_var1, key_var2),
                new InvConUserBookkeeping2(main_keys_var, sub_keys_var, sub_lengths_var, values_var,
                key_var2, key_var1)
                };
            }else{
                return null;
            }
        }else{
            return null;
        }
    }
    
}
