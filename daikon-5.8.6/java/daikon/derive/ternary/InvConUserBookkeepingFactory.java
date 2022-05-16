package daikon.derive.ternary;

import daikon.ProglangType;
import daikon.VarInfo;
import org.checkerframework.checker.nullness.qual.Nullable;

public class InvConUserBookkeepingFactory extends TernaryDerivationFactory {

    public boolean isKeyValuePair(VarInfo vi1, VarInfo vi2){
       return vi1.isArray() && vi2.isArray() 
        && (vi2.get_enclosing_var().name().equals(vi1.name())) && (vi2.name().contains("Sub")!=true); 
    }

    @Override
    public TernaryDerivation @Nullable [] instantiate(VarInfo vi1, VarInfo vi2, VarInfo vi3) {
        // TODO Auto-generated method stub
        
        // System.out.println("InvConUserBookkeepingFactory.instantiate(" + vi1.rep_type + " " +   vi2.rep_type + " " +   vi3.rep_type + ")");
        // System.out.println("InvConUserBookkeeping.dkconfig_enabled: "+ InvConUserBookkeeping.dkconfig_enabled);
        
        // check if the derivations are globally disabled
        boolean enable_bookkeeping = InvConUserBookkeeping.dkconfig_enabled;
        if (!enable_bookkeeping) {
            return null;
        }

        VarInfo enclose_keys_var;
        VarInfo values_var;
        VarInfo key_var;


        if(isKeyValuePair(vi1, vi2) && !vi3.rep_type.isArray() && vi1.rep_type.base().equals(vi3.rep_type.base())){
            enclose_keys_var = vi1;
            values_var = vi2;
            key_var = vi3;
        }
        else if(isKeyValuePair(vi2, vi1) && !vi3.rep_type.isArray() && vi2.rep_type.base().equals(vi3.rep_type.base())){
            enclose_keys_var = vi2;
            values_var = vi1;
            key_var = vi3;
        }
        else if(isKeyValuePair(vi1, vi3) && !vi2.rep_type.isArray() && vi1.rep_type.base().equals(vi2.rep_type.base())){
            enclose_keys_var = vi1;
            values_var = vi3;
            key_var = vi2;
        }
        else if(isKeyValuePair(vi3, vi1) && !vi2.rep_type.isArray() && vi3.rep_type.base().equals(vi2.rep_type.base())){
            enclose_keys_var = vi3;
            values_var = vi1;
            key_var = vi2;
        }
        else if(isKeyValuePair(vi2, vi3) && !vi1.rep_type.isArray() && vi2.rep_type.base().equals(vi1.rep_type.base())){
            enclose_keys_var = vi2;
            values_var = vi3;
            key_var = vi1;
        }
        else if(isKeyValuePair(vi3, vi2) && !vi1.rep_type.isArray() && vi3.rep_type.base().equals(vi1.rep_type.base())){
            enclose_keys_var = vi3;
            values_var = vi2;
            key_var = vi1;
        }else{
            return null;
        }
        
        // VarInfo String_Array = null;
        // VarInfo Double_Array = null;
        // VarInfo StringVar = null;

        // if (vi1.rep_type ==  ProglangType.STRING_ARRAY){
        //     String_Array = vi1;
        // }else
        // if (vi2.rep_type ==  ProglangType.STRING_ARRAY){
        //     String_Array = vi2;
        // }else 
        // if (vi3.rep_type ==  ProglangType.STRING_ARRAY){
        //     String_Array = vi3;
        // }

        // if (vi1.rep_type ==  ProglangType.DOUBLE_ARRAY || vi1.rep_type ==  ProglangType.BIGINT_ARRAY){
        //     Double_Array = vi1;
        // }else
        // if (vi2.rep_type ==  ProglangType.DOUBLE_ARRAY || vi2.rep_type ==  ProglangType.BIGINT_ARRAY){
        //     Double_Array = vi2;
        // }else 
        // if (vi3.rep_type ==  ProglangType.DOUBLE_ARRAY || vi3.rep_type ==  ProglangType.BIGINT_ARRAY){
        //     Double_Array = vi3;
        // }

        // if (vi1.rep_type ==  ProglangType.STRING){
        //     StringVar = vi1;
        // }else
        // if (vi2.rep_type ==  ProglangType.STRING){
        //     StringVar = vi2;
        // }else 
        // if (vi3.rep_type ==  ProglangType.STRING){
        //     StringVar = vi3;
        // }

        // if (String_Array == null || Double_Array == null || StringVar == null){
        //     return null;
        // }else{
        //     if ( !(Double_Array.get_enclosing_var().name().equals(String_Array.name()))  || (Double_Array.name().contains("Sub")==true) ){
        //         return null; 
        //     }else{
        //         enclose_keys_var =  String_Array;
        //         values_var = Double_Array;
        //         key_var = StringVar;
        //         // System.out.println("");
        //         // System.out.println(enclose_keys_var);
        //         // System.out.println(values_var);
        //         // System.out.println(key_var);
        //     }
        // }

        return new TernaryDerivation[]{
            new InvConUserBookkeeping(enclose_keys_var, values_var, key_var)
        };
    }
    
}
